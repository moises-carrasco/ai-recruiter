"""
Interview service for interview management and execution operations.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..repositories.interview_repo import (
    InterviewRepository,
    InterviewTranscriptRepository,
    InterviewFeedbackRepository
)
from ..schemas.interview import (
    InterviewCreate,
    InterviewUpdate,
    InterviewOut,
    InterviewListResponse,
    InterviewFilter,
    InterviewWithFeedbackOut,
    InterviewStartRequest,
    InterviewCompleteRequest,
    InterviewTranscriptOut,
    InterviewFeedbackOut
)
from ..utils.link_generator import (
    generate_unique_interview_link,
    validate_link_expiration,
    generate_link_expiration_datetime
)
from ..utils.file_handler import FileHandler
from ..models.lookup import LookupItem
from ..models.user import User
from ..models.candidate import Candidate
from ..core.logging_config import get_logger
from .ai_agent_service import AIAgentService


class InterviewService:
    """Service for interview-related business operations."""

    def __init__(self):
        self.interview_repo = InterviewRepository()
        self.transcript_repo = InterviewTranscriptRepository()
        self.feedback_repo = InterviewFeedbackRepository()
        self.logger = get_logger(__name__)

    async def create_interview(self, db: Session, interview_data: InterviewCreate) -> InterviewOut:
        """Create a new interview with generated link and validation."""
        # Validate foreign key references
        await self._validate_interview_references(db, interview_data)

        # Generate unique interview link
        # Note: We'll generate this after creation since we need the interview ID
        interview_dict = interview_data.model_dump()

        # Set initial status if not provided (assume 'registered' status)
        if not interview_dict.get('status_id'):
            registered_status = db.query(LookupItem).filter(
                LookupItem.domain_id == 'interview_status',
                LookupItem.item_id == 'registered'
            ).first()
            if registered_status:
                interview_dict['status_id'] = registered_status.id

        # Create interview
        interview = await self.interview_repo.create(db, interview_dict)

        # Generate and update interview link
        interview_link = generate_unique_interview_link(interview.id)
        link_expires_at = generate_link_expiration_datetime(interview.scheduled_datetime)

        update_data = {
            'interview_link': interview_link,
            'link_expires_at': link_expires_at
        }
        interview = await self.interview_repo.update(db, interview, update_data)

        return await self._enrich_interview_data(db, interview)

    async def get_interview_by_id(self, db: Session, interview_id: int) -> InterviewOut:
        """Get interview by ID with related data."""
        interview = await self.interview_repo.get_by_id(db, interview_id)
        if not interview:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found"
            )
        return await self._enrich_interview_data(db, interview)

    async def get_interview_by_link(self, db: Session, interview_link: str) -> InterviewOut:
        """Get interview by unique link for candidate access."""
        # Add "interview/" prefix to match database format
        full_link = f"interview/{interview_link}"
        print(f"DEBUG: Searching for interview with link: {full_link}")
        interview = self.interview_repo.get_by_link(db, full_link)

        if not interview:
            print(f"DEBUG: Interview not found for link: {full_link}")
            # Let's also check if there are any interviews at all
            all_interviews = db.query(self.interview_repo.model).limit(5).all()
            print(f"DEBUG: Sample interviews in DB: {[f'{i.id}: {i.interview_link}' for i in all_interviews]}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview link not found or invalid"
            )

        print(f"DEBUG: Found interview: {interview.id} with link: {interview.interview_link}")

        # Note: Date/time validation removed as per user request
        # Validate link expiration (commented out)
        # if not validate_link_expiration(interview.scheduled_datetime):
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Interview link has expired"
        #     )

        return await self._enrich_interview_data(db, interview)

    async def update_interview(
        self,
        db: Session,
        interview_id: int,
        interview_data: InterviewUpdate
    ) -> InterviewOut:
        """Update an existing interview."""
        # Get the SQLAlchemy model directly from repository
        interview_model = await self.interview_repo.get_by_id(db, interview_id)
        if not interview_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found"
            )

        # Validate references if they're being updated
        if any(key in interview_data.model_dump(exclude_unset=True)
               for key in ['analyst_id', 'candidate_id', 'role_id', 'seniority_id', 'client_id']):
            await self._validate_interview_references(db, interview_data, exclude_id=interview_id)

        update_dict = interview_data.model_dump(exclude_unset=True)
        updated_interview = await self.interview_repo.update(db, interview_model, update_dict)

        return await self._enrich_interview_data(db, updated_interview)

    async def delete_interview(self, db: Session, interview_id: int) -> None:
        """Delete an interview (soft delete if applicable)."""
        interview = await self.get_interview_by_id(db, interview_id)

        # Clean up associated files before deleting
        if interview.cv_file_path:
            FileHandler.delete_file(interview.cv_file_path)
        if interview.job_description_path:
            FileHandler.delete_file(interview.job_description_path)

        await self.interview_repo.delete(db, interview_id)

    async def list_interviews(
        self,
        db: Session,
        filters: InterviewFilter
    ) -> InterviewListResponse:
        """List interviews with filtering and pagination."""
        filter_dict = filters.model_dump(exclude={'page', 'per_page'})
        skip = (filters.page - 1) * filters.per_page

        interviews = await self.interview_repo.get_interviews_with_filters(
            db, filter_dict, skip, filters.per_page
        )
        total_count = await self.interview_repo.count_interviews_with_filters(db, filter_dict)
        total_pages = (total_count + filters.per_page - 1) // filters.per_page

        # Enrich interview data
        enriched_interviews = []
        for interview in interviews:
            enriched_interviews.append(await self._enrich_interview_data(db, interview))

        return InterviewListResponse(
            interviews=enriched_interviews,
            total=total_count,
            page=filters.page,
            per_page=filters.per_page,
            total_pages=total_pages
        )

    async def filter_interviews_by_role_and_client(
        self,
        db: Session,
        role_id: Optional[int] = None,
        client_id: Optional[int] = None,
        page: int = 1,
        per_page: int = 20
    ) -> InterviewListResponse:
        """Filter interviews by role and/or client."""
        skip = (page - 1) * per_page

        interviews = await self.interview_repo.filter_by_role_and_client(
            db, role_id, client_id, skip, per_page
        )

        # Count total (simplified - could be optimized)
        total_count = len(await self.interview_repo.filter_by_role_and_client(
            db, role_id, client_id, 0, 10000  # Large limit for count
        ))

        total_pages = (total_count + per_page - 1) // per_page

        # Enrich interview data
        enriched_interviews = []
        for interview in interviews:
            enriched_interviews.append(await self._enrich_interview_data(db, interview))

        return InterviewListResponse(
            interviews=enriched_interviews,
            total=total_count,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )

    async def validate_interview_access(self, db: Session, interview_link: str) -> bool:
        """Validate if interview link is accessible."""
        try:
            interview = await self.get_interview_by_link(db, interview_link)
            return True
        except HTTPException:
            return False

    async def start_interview(
        self,
        db: Session,
        interview_id: int,
        start_request: InterviewStartRequest
    ) -> InterviewWithFeedbackOut:
        """Start an interview session."""
        interview = await self.get_interview_by_id(db, interview_id)

        # Update status to 'executed' if it's currently 'registered'
        executed_status = db.query(LookupItem).filter(
            LookupItem.domain_id == 'interview_status',
            LookupItem.item_id == 'executed'
        ).first()

        if executed_status and interview.status_id != executed_status.id:
            await self.interview_repo.update(db, interview, {'status_id': executed_status.id})
            interview.status_id = executed_status.id

        # Create or update transcript with start time
        transcript = self.transcript_repo.get_by_interview_id(db, interview_id)
        if not transcript:
            transcript_data = {
                'interview_id': interview_id,
                'transcript_content': '',
                'started_at': datetime.utcnow().isoformat()
            }
            transcript = self.transcript_repo.create(db, transcript_data)
        elif not transcript.started_at:
            self.transcript_repo.update(db, transcript, {
                'started_at': datetime.utcnow().isoformat()
            })

        return await self._get_interview_with_feedback(db, interview_id)

    async def complete_interview(
        self,
        db: Session,
        interview_id: int,
        complete_request: InterviewCompleteRequest
    ) -> InterviewWithFeedbackOut:
        """Complete an interview and generate feedback."""
        interview = await self.get_interview_by_id(db, interview_id)

        # Update status to 'completed'
        completed_status = db.query(LookupItem).filter(
            LookupItem.domain_id == 'interview_status',
            LookupItem.item_id == 'completed'
        ).first()

        if completed_status:
            await self.interview_repo.update(db, interview, {'status_id': completed_status.id})

        # Update transcript with completion
        transcript = self.transcript_repo.get_by_interview_id(db, interview_id)
        if transcript:
            update_data = {
                'transcript_content': complete_request.transcript_content,
                'completed_at': datetime.utcnow().isoformat()
            }
            self.transcript_repo.update(db, transcript, update_data)

        # TODO: Generate AI feedback
        # For now, create placeholder feedback
        feedback = self.feedback_repo.get_by_interview_id(db, interview_id)
        if not feedback:
            feedback_data = {
                'interview_id': interview_id,
                'general_comments': 'Interview completed. AI feedback generation pending.',
                'overall_ranking': 3,
                'skills_evaluation': '[]',  # Empty JSON array
                'strengths': None,
                'areas_for_improvement': None,
                'job_fit_assessment': None
            }
            self.feedback_repo.create(db, feedback_data)

        return await self._get_interview_with_feedback(db, interview_id)

    async def get_interview_feedback(self, db: Session, interview_id: int) -> Optional[InterviewFeedbackOut]:
        """Get feedback for a specific interview."""
        feedback = self.feedback_repo.get_by_interview_id(db, interview_id)
        if feedback:
            return InterviewFeedbackOut.model_validate(feedback)
        return None

    async def get_interview_transcript(self, db: Session, interview_id: int) -> Optional[InterviewTranscriptOut]:
        """Get transcript for a specific interview."""
        transcript = self.transcript_repo.get_by_interview_id(db, interview_id)
        if transcript:
            return InterviewTranscriptOut.model_validate(transcript)
        return None

    async def get_interview_transcripts(self, db: Session, interview_id: int) -> List[InterviewTranscriptOut]:
        """Get all transcripts for a specific interview ordered by started_at and id."""
        transcripts = db.query(self.transcript_repo.model).filter(
            self.transcript_repo.model.interview_id == interview_id
        ).order_by(self.transcript_repo.model.started_at, self.transcript_repo.model.id).all()

        return [InterviewTranscriptOut.model_validate(transcript) for transcript in transcripts]

    async def _validate_interview_references(
        self,
        db: Session,
        interview_data: InterviewCreate | InterviewUpdate,
        exclude_id: Optional[int] = None
    ) -> None:
        """Validate foreign key references in interview data."""
        data_dict = interview_data.model_dump()

        # Validate analyst exists and is active
        if data_dict.get('analyst_id'):
            analyst = db.query(User).filter(
                User.id == data_dict['analyst_id'],
                User.is_active == True
            ).first()
            if not analyst:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid analyst ID"
                )

        # Validate candidate exists and is active
        if data_dict.get('candidate_id'):
            candidate = db.query(Candidate).filter(
                Candidate.id == data_dict['candidate_id'],
                Candidate.is_active == True
            ).first()
            if not candidate:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid candidate ID"
                )

        # Validate lookup items exist
        lookup_fields = ['role_id', 'seniority_id', 'client_id', 'status_id']
        for field in lookup_fields:
            if data_dict.get(field):
                lookup_item = db.query(LookupItem).filter(
                    LookupItem.id == data_dict[field],
                    LookupItem.is_active == True
                ).first()
                if not lookup_item:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid {field}"
                    )

        # Validate scheduled datetime is in the future
        if hasattr(interview_data, 'scheduled_datetime') and interview_data.scheduled_datetime:
            scheduled = datetime.fromisoformat(interview_data.scheduled_datetime.replace('Z', '+00:00'))
            if scheduled <= datetime.now(timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Interview must be scheduled in the future"
                )

    async def _enrich_interview_data(self, db: Session, interview) -> InterviewOut:
        """Enrich interview data with related information."""
        # Get related names
        analyst = db.query(User).filter(User.id == interview.analyst_id).first()
        candidate = db.query(Candidate).filter(Candidate.id == interview.candidate_id).first()

        role = db.query(LookupItem).filter(LookupItem.id == interview.role_id).first()
        seniority = db.query(LookupItem).filter(LookupItem.id == interview.seniority_id).first()
        client = db.query(LookupItem).filter(LookupItem.id == interview.client_id).first() if interview.client_id else None
        status_item = db.query(LookupItem).filter(LookupItem.id == interview.status_id).first()

        # Create enriched output
        interview_dict = InterviewOut.model_validate(interview).model_dump()
        interview_dict.update({
            'analyst_name': f"{analyst.first_name} {analyst.last_name}" if analyst else None,
            'candidate_name': f"{candidate.first_name} {candidate.last_name}" if candidate else None,
            'role_text': role.text_value if role else None,
            'seniority_text': seniority.text_value if seniority else None,
            'client_text': client.text_value if client else None,
            'status_text': status_item.text_value if status_item else None,
        })

        return InterviewOut(**interview_dict)

    def get_message_payload_interview(self, db: Session, interview_id: int) -> Dict[str, Any]:
        """Get conversation payload for AI service in the expected format."""
        transcripts = db.query(self.transcript_repo.model).filter(
            self.transcript_repo.model.interview_id == interview_id
        ).order_by(self.transcript_repo.model.started_at, self.transcript_repo.model.id).all()

        messages = []
        for transcript in transcripts:
            # Map roles: 'candidate' or 'system' -> 'user', 'assistant' -> 'assistant'
            role = 'user' if transcript.role in ['candidate', 'system'] else 'assistant'
            messages.append({
                'role': role,
                'content': transcript.transcript_content
            })

        return {
            'model': 'saia:assistant:Interviewer_Expert',
            'messages': messages,
            'revision': 3,
            'revisionName': '3'
        }

    async def send_chat_message(self, db: Session, interview_id: int, message_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a chat message based on message_type.

        Returns different response structures based on message_type:
        - start_interview: Returns filtered conversation history
        - candidate_answer: Returns last assistant message
        """
        message_type = message_request.get('message_type')
        message = message_request.get('message')
        current_time = datetime.utcnow().isoformat()

        # Get conversation history
        conversation_history_list = self.transcript_repo.get_messages_by_interview_id(db, interview_id)
        is_new_conversation = len(conversation_history_list) == 0

        if message_type == 'start_interview' and is_new_conversation:
            # Get interview data for kickoff message
            interview = await self.get_interview_by_id(db, interview_id)

            # Read job description and CV file contents
            job_description_content = self._read_file_content_safe(interview.job_description_path)
            cv_content = self._read_file_content_safe(interview.cv_file_path)

            # Create kickoff system message
            kickoff_msg = f"""Hi Interviewer_Expert you are just about to start a new interview with a candidate. Here is the data:
<========= candidate_name =========>
{interview.candidate_name}
<=========  seniority =========>
{interview.seniority_text}
<========= role =========>
{interview.role_text}
<========= job_description =========>
{job_description_content}
<========= cv =========>
{cv_content}
<========= end =========>

This data is just internal information and it represents the parameter that you will be using to conduct the interview.
Please remember to start the interview by saying hello to the candidate and introducing yourself"""

            # Log kickoff message for debugging
            self.logger.info(f"Kickoff message for interview {interview_id}: {kickoff_msg}")

            # Store system message
            system_transcript = {
                'interview_id': interview_id,
                'transcript_content': kickoff_msg,
                'role': 'system',
                'started_at': current_time,
                'completed_at': current_time
            }
            await self.transcript_repo.create(db, system_transcript)

            # Refresh conversation history after adding system message
            conversation_history_list = self.transcript_repo.get_messages_by_interview_id(db, interview_id)

            # Format payload for AI
            conversation_payload = self._format_messages_payload_ai(conversation_history_list)

            # Send to AI service
            ai_service = AIAgentService()
            ai_response = await ai_service.send_chat_message(conversation_payload)

            # Check if AI response was successful
            if ai_response.get('status') != 'succeeded':
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="AI service error: " + ai_response.get('error', 'Unknown error')
                )

            # Extract and store AI response
            message_from_ai = ai_response.get('text', '')
            ai_transcript = {
                'interview_id': interview_id,
                'transcript_content': message_from_ai,
                'role': 'assistant',
                'started_at': current_time,
                'completed_at': current_time
            }
            await self.transcript_repo.create(db, ai_transcript)

        elif message_type == 'candidate_answer':
            # Store candidate message
            candidate_transcript = {
                'interview_id': interview_id,
                'transcript_content': message,
                'role': 'candidate',
                'started_at': current_time,
                'completed_at': current_time
            }
            await self.transcript_repo.create(db, candidate_transcript)

            # Refresh conversation history after adding candidate message
            conversation_history_list = self.transcript_repo.get_messages_by_interview_id(db, interview_id)

            # Format payload for AI
            conversation_payload = self._format_messages_payload_ai(conversation_history_list)

            # Send to AI service
            ai_service = AIAgentService()
            ai_response = await ai_service.send_chat_message(conversation_payload)

            # Check if AI response was successful
            if ai_response.get('status') != 'succeeded':
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="AI service error: " + ai_response.get('error', 'Unknown error')
                )

            # Extract and store AI response
            message_from_ai = ai_response.get('text', '')
            ai_transcript = {
                'interview_id': interview_id,
                'transcript_content': message_from_ai,
                'role': 'assistant',
                'started_at': current_time,
                'completed_at': current_time
            }
            await self.transcript_repo.create(db, ai_transcript)

        # Refresh conversation history after processing message
        conversation_history_list = self.transcript_repo.get_messages_by_interview_id(db, interview_id)

        # Filter messages to only include candidate and assistant roles
        filtered_conversation_history = self._filter_messages_only(conversation_history_list, roles=['candidate', 'assistant'])

        print(f"DEBUG: Filtered conversation history has {len(filtered_conversation_history)} messages")
        for msg in filtered_conversation_history:
            print(f"DEBUG: Message {msg.id}: role={msg.role}, content_preview='{msg.transcript_content[:50]}...'")

        if message_type == 'start_interview':
            # Return the whole filtered conversation history
            return {
                'conversation_history': [
                    {
                        'id': msg.id,
                        'content': msg.transcript_content,
                        'role': msg.role,
                        'started_at': msg.started_at
                    } for msg in filtered_conversation_history
                ]
            }
        elif message_type == 'candidate_answer':
            # Get the last assistant message
            assistant_messages = [msg for msg in filtered_conversation_history if msg.role == 'assistant']
            print(f"DEBUG: Found {len(assistant_messages)} assistant messages")

            if assistant_messages:
                last_message = assistant_messages[-1]
                print(f"DEBUG: Returning last assistant message: id={last_message.id}, content_preview='{last_message.transcript_content[:50]}...'")
                return {
                    'last_message': {
                        'id': last_message.id,
                        'content': last_message.transcript_content,
                        'role': last_message.role,
                        'started_at': last_message.started_at
                    }
                }
            else:
                print("DEBUG: No assistant messages found!")
                return {'last_message': None}

        # Default response
        return {'conversation_history': []}

    def _filter_messages_only(self, conversation_history_list: List, roles: List[str]) -> List:
        """Filter messages to only include specified roles."""
        return [msg for msg in conversation_history_list if msg.role in roles]

    def _format_messages_payload_ai(self, conversation_history_list: List) -> Dict[str, Any]:
        """Format messages for AI service payload."""
        messages = []
        for transcript in conversation_history_list:
            # Map roles: 'candidate' or 'system' -> 'user', 'assistant' -> 'assistant'
            role = 'user' if transcript.role in ['candidate', 'system'] else 'assistant'
            messages.append({
                'role': role,
                'content': transcript.transcript_content
            })

        return {
            'assistant': 'Interviewer_Expert',
            'messages': messages,
            'revision': 3,
            'revisionName': '3'
        }

    def _read_file_content_safe(self, relative_path: Optional[str]) -> str:
        """Safely read file content with error handling and length limiting.

        Args:
            relative_path: Relative path to the file from project root

        Returns:
            File content (max 2000 chars) or error message
        """
        if not relative_path:
            return "Not provided"

        try:
            # Build full path: project_root + relative_path
            project_root = Path(__file__).resolve().parent.parent.parent.parent
            full_path = project_root / relative_path
            content = FileHandler.read_file_content(str(full_path))[:2000]  # Limit to 2000 chars
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"

    async def _get_interview_with_feedback(self, db: Session, interview_id: int) -> InterviewWithFeedbackOut:
        """Get interview with associated feedback and transcript."""
        interview = await self.get_interview_by_id(db, interview_id)
        feedback = await self.get_interview_feedback(db, interview_id)
        transcript = await self.get_interview_transcript(db, interview_id)

        interview_dict = interview.model_dump()
        interview_dict['feedback'] = feedback
        interview_dict['transcript'] = transcript

        return InterviewWithFeedbackOut(**interview_dict)
