"""
Interview service for interview management and execution operations.
"""

from datetime import datetime, timezone
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
from ..models.lookup import LookupItem
from ..models.user import User
from ..models.candidate import Candidate


class InterviewService:
    """Service for interview-related business operations."""

    def __init__(self):
        self.interview_repo = InterviewRepository()
        self.transcript_repo = InterviewTranscriptRepository()
        self.feedback_repo = InterviewFeedbackRepository()

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
        interview = self.interview_repo.get_by_link(db, full_link)

        if not interview:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview link not found or invalid"
            )

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
        interview = await self.get_interview_by_id(db, interview_id)

        # Validate references if they're being updated
        if any(key in interview_data.model_dump(exclude_unset=True)
               for key in ['analyst_id', 'candidate_id', 'role_id', 'seniority_id', 'client_id']):
            await self._validate_interview_references(db, interview_data, exclude_id=interview_id)

        update_dict = interview_data.model_dump(exclude_unset=True)
        updated_interview = await self.interview_repo.update(db, interview, update_dict)

        return await self._enrich_interview_data(db, updated_interview)

    async def delete_interview(self, db: Session, interview_id: int) -> None:
        """Delete an interview (soft delete if applicable)."""
        interview = await self.get_interview_by_id(db, interview_id)
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
        """Get all transcripts for a specific interview ordered by created_at."""
        transcripts = db.query(self.transcript_repo.model).filter(
            self.transcript_repo.model.interview_id == interview_id
        ).order_by(self.transcript_repo.model.created_at).all()

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

    async def send_chat_message(self, db: Session, interview_id: int, message: str) -> str:
        """Send a chat message and return AI response (echo for now)."""
        current_time = datetime.utcnow().isoformat()

        # Save candidate message
        candidate_transcript = {
            'interview_id': interview_id,
            'transcript_content': message,
            'role': 'candidate',
            'started_at': current_time,
            'completed_at': current_time
        }
        await self.transcript_repo.create(db, candidate_transcript)

        # Generate AI response (simple echo for now)
        ai_response = message  # Echo the user's message

        # Save AI response
        ai_transcript = {
            'interview_id': interview_id,
            'transcript_content': ai_response,
            'role': 'assistant',
            'started_at': current_time,
            'completed_at': current_time
        }
        await self.transcript_repo.create(db, ai_transcript)

        return ai_response

    async def _get_interview_with_feedback(self, db: Session, interview_id: int) -> InterviewWithFeedbackOut:
        """Get interview with associated feedback and transcript."""
        interview = await self.get_interview_by_id(db, interview_id)
        feedback = await self.get_interview_feedback(db, interview_id)
        transcript = await self.get_interview_transcript(db, interview_id)

        interview_dict = interview.model_dump()
        interview_dict['feedback'] = feedback
        interview_dict['transcript'] = transcript

        return InterviewWithFeedbackOut(**interview_dict)
