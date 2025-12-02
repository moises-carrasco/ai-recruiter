"""
Interview management and execution routes.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.interview_service import InterviewService
from app.schemas.interview import (
    InterviewCreate,
    InterviewUpdate,
    InterviewOut,
    InterviewListResponse,
    InterviewFilter,
    InterviewWithFeedbackOut,
    InterviewStartRequest,
    InterviewCompleteRequest,
    InterviewFeedbackOut,
    InterviewTranscriptOut,
    InterviewTranscriptsList,
    ChatMessageRequest
)
from app.utils.file_handler import FileHandler
from pathlib import Path

router = APIRouter()


def get_interview_service() -> InterviewService:
    """Dependency to get interview service."""
    return InterviewService()


@router.get("/health", status_code=status.HTTP_200_OK)
async def interviews_health():
    """Health check for interviews module."""
    return {"status": "ok", "module": "interviews"}


@router.get("/", response_model=InterviewListResponse, status_code=status.HTTP_200_OK)
async def list_interviews(
    analyst_id: Optional[int] = Query(None, description="Filter by analyst ID"),
    candidate_id: Optional[int] = Query(None, description="Filter by candidate ID"),
    role_id: Optional[int] = Query(None, description="Filter by role ID"),
    client_id: Optional[int] = Query(None, description="Filter by client ID"),
    status_id: Optional[int] = Query(None, description="Filter by status ID"),
    scheduled_from: Optional[str] = Query(None, description="Filter interviews scheduled from this date (ISO8601)"),
    scheduled_to: Optional[str] = Query(None, description="Filter interviews scheduled to this date (ISO8601)"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Get list of interviews with filtering and pagination.

    - **analyst_id**: Filter by analyst who created the interview
    - **candidate_id**: Filter by candidate
    - **role_id**: Filter by job role
    - **client_id**: Filter by client
    - **status_id**: Filter by interview status
    - **scheduled_from**: Filter interviews scheduled from this date
    - **scheduled_to**: Filter interviews scheduled to this date
    - **page**: Page number for pagination (default: 1)
    - **per_page**: Number of items per page (default: 20, max: 100)
    """
    filters = InterviewFilter(
        analyst_id=analyst_id,
        candidate_id=candidate_id,
        role_id=role_id,
        client_id=client_id,
        status_id=status_id,
        scheduled_from=scheduled_from,
        scheduled_to=scheduled_to,
        page=page,
        per_page=per_page
    )
    return await service.list_interviews(db, filters)


@router.post("/", response_model=InterviewOut, status_code=status.HTTP_201_CREATED)
async def create_interview(
    interview_data: InterviewCreate,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Create a new interview.

    - **analyst_id**: ID of the recruiting analyst (required)
    - **candidate_id**: ID of the candidate (required)
    - **role_id**: ID of the job role (required)
    - **seniority_id**: ID of the seniority level (required)
    - **client_id**: ID of the client (optional)
    - **cv_file_path**: Path to uploaded CV file (optional)
    - **job_description_path**: Path to uploaded job description file (optional)
    - **interview_guidelines**: Specific guidelines for the interview (optional)
    - **scheduled_datetime**: Scheduled date and time in ISO8601 format (required)
    - **status_id**: ID of the interview status (required)
    - **notes**: Additional notes (optional)
    """
    return await service.create_interview(db, interview_data)


@router.get("/{interview_id}", response_model=InterviewOut, status_code=status.HTTP_200_OK)
async def get_interview_by_id(
    interview_id: int,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Get a specific interview by ID.

    - **interview_id**: The ID of the interview to retrieve
    """
    return await service.get_interview_by_id(db, interview_id)


@router.put("/{interview_id}", response_model=InterviewOut, status_code=status.HTTP_200_OK)
async def update_interview(
    interview_id: int,
    interview_data: InterviewUpdate,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Update an existing interview.

    - **interview_id**: The ID of the interview to update
    - **analyst_id**: Updated analyst ID (optional)
    - **candidate_id**: Updated candidate ID (optional)
    - **role_id**: Updated role ID (optional)
    - **seniority_id**: Updated seniority ID (optional)
    - **client_id**: Updated client ID (optional)
    - **cv_file_path**: Updated CV file path (optional)
    - **job_description_path**: Updated job description path (optional)
    - **interview_guidelines**: Updated guidelines (optional)
    - **scheduled_datetime**: Updated scheduled datetime (optional)
    - **status_id**: Updated status ID (optional)
    - **notes**: Updated notes (optional)
    """
    return await service.update_interview(db, interview_id, interview_data)


@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Delete an interview.

    - **interview_id**: The ID of the interview to delete
    """
    await service.delete_interview(db, interview_id)


@router.get("/link/{interview_link}", response_model=InterviewOut, status_code=status.HTTP_200_OK)
async def get_interview_by_link(
    interview_link: str,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Access interview by unique link (for candidates).

    - **interview_link**: The unique interview link
    """
    return await service.get_interview_by_link(db, interview_link)


@router.post("/{interview_id}/start", response_model=InterviewWithFeedbackOut, status_code=status.HTTP_200_OK)
async def start_interview(
    interview_id: int,
    start_request: InterviewStartRequest,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Start an interview session.

    - **interview_id**: The ID of the interview to start
    """
    return await service.start_interview(db, interview_id, start_request)


@router.post("/{interview_id}/complete", response_model=InterviewWithFeedbackOut, status_code=status.HTTP_200_OK)
async def complete_interview(
    interview_id: int,
    complete_request: InterviewCompleteRequest,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Complete an interview and generate feedback.

    - **interview_id**: The ID of the interview to complete
    - **transcript_content**: Complete interview conversation transcript
    """
    return await service.complete_interview(db, interview_id, complete_request)


@router.get("/{interview_id}/feedback", response_model=InterviewFeedbackOut, status_code=status.HTTP_200_OK)
async def get_interview_feedback(
    interview_id: int,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Get feedback for a specific interview.

    - **interview_id**: The ID of the interview
    """
    feedback = await service.get_interview_feedback(db, interview_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview feedback not found"
        )
    return feedback


@router.get("/{interview_id}/transcript", response_model=InterviewTranscriptOut, status_code=status.HTTP_200_OK)
async def get_interview_transcript(
    interview_id: int,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Get transcript for a specific interview.

    - **interview_id**: The ID of the interview
    """
    transcript = await service.get_interview_transcript(db, interview_id)
    if not transcript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview transcript not found"
        )
    return transcript


@router.post("/link/{interview_link}/chat", status_code=status.HTTP_200_OK)
async def send_chat_message(
    interview_link: str,
    message_request: ChatMessageRequest,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Send a chat message during interview.

    Returns different response structures based on message_type:
    - start_interview: Returns conversation_history with filtered messages
    - candidate_answer: Returns last_message with the AI response

    - **interview_link**: The interview link hash
    - **message_type**: Type of message ('start_interview' or 'candidate_answer')
    - **message**: The message content (required for candidate_answer)
    """
    # Get the interview by link to obtain the numeric ID
    interview = await service.get_interview_by_link(db, interview_link)
    response = await service.send_chat_message(db, interview.id, message_request.model_dump())
    return response


@router.get("/link/{interview_link}/transcripts", response_model=InterviewTranscriptsList, status_code=status.HTTP_200_OK)
async def get_interview_transcripts(
    interview_link: str,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Get all transcripts for an interview ordered by created_at.

    - **interview_link**: The interview link hash
    """
    # Get the interview by link to obtain the numeric ID
    interview = await service.get_interview_by_link(db, interview_link)
    transcripts = await service.get_interview_transcripts(db, interview.id)
    return InterviewTranscriptsList(transcripts=transcripts)


@router.get("/filter/by-role-client", response_model=InterviewListResponse, status_code=status.HTTP_200_OK)
async def filter_interviews_by_role_and_client(
    role_id: Optional[int] = Query(None, description="Filter by role ID"),
    client_id: Optional[int] = Query(None, description="Filter by client ID"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Filter interviews by role and/or client.

    - **role_id**: Filter by job role
    - **client_id**: Filter by client
    - **page**: Page number for pagination (default: 1)
    - **per_page**: Number of items per page (default: 20, max: 100)
    """
    return await service.filter_interviews_by_role_and_client(
        db, role_id, client_id, page, per_page
    )


# File upload and download endpoints

@router.post("/{interview_id}/upload-cv", status_code=status.HTTP_200_OK)
async def upload_cv_file(
    interview_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Upload CV file for an interview.

    - **interview_id**: The ID of the interview
    - **file**: The CV file to upload (only .txt and .md files allowed)
    """
    # Get interview model directly from repository to validate and get candidate_id
    interview_repo = service.interview_repo
    interview = await interview_repo.get_by_id(db, interview_id)
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    # Save file and get path (delete existing file if present)
    # Convert existing path to absolute for proper deletion
    existing_path = FileHandler.get_absolute_path(interview.cv_file_path) if interview.cv_file_path else None
    file_path = await FileHandler.save_cv_file(file, interview.candidate_id, interview_id, existing_path)

    # Update interview with file path
    update_data = InterviewUpdate(cv_file_path=file_path)
    updated_interview = await service.update_interview(db, interview_id, update_data)

    return {"message": "CV file uploaded successfully", "file_path": file_path}


@router.post("/{interview_id}/upload-job-description", status_code=status.HTTP_200_OK)
async def upload_job_description_file(
    interview_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Upload job description file for an interview.

    - **interview_id**: The ID of the interview
    - **file**: The job description file to upload (only .txt and .md files allowed)
    """
    # Get interview model directly from repository to check for existing file
    interview_repo = service.interview_repo
    interview = await interview_repo.get_by_id(db, interview_id)
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )

    # Save file and get path (delete existing file if present)
    # Convert existing path to absolute for proper deletion
    existing_path = FileHandler.get_absolute_path(interview.job_description_path) if interview.job_description_path else None
    file_path = await FileHandler.save_job_description_file(file, interview_id, existing_path)

    # Update interview with file path
    update_data = InterviewUpdate(job_description_path=file_path)
    updated_interview = await service.update_interview(db, interview_id, update_data)

    return {"message": "Job description file uploaded successfully", "file_path": file_path}


@router.get("/{interview_id}/download-cv")
async def download_cv_file(
    interview_id: int,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Download CV file for an interview.

    - **interview_id**: The ID of the interview
    """
    interview = await service.get_interview_by_id(db, interview_id)

    if not interview.cv_file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV file not found for this interview"
        )

    # Convert relative path to absolute path
    absolute_path = FileHandler.get_absolute_path(interview.cv_file_path)

    if not FileHandler.file_exists(absolute_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV file not found on disk"
        )

    # Get file extension from the saved file
    file_extension = Path(interview.cv_file_path).suffix or '.txt'

    # Return file as download
    return FileResponse(
        path=absolute_path,
        media_type='text/plain',
        filename=f"cv_interview_{interview_id}{file_extension}"
    )


@router.get("/{interview_id}/download-job-description")
async def download_job_description_file(
    interview_id: int,
    db: Session = Depends(get_db),
    service: InterviewService = Depends(get_interview_service)
):
    """
    Download job description file for an interview.

    - **interview_id**: The ID of the interview
    """
    interview = await service.get_interview_by_id(db, interview_id)

    if not interview.job_description_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description file not found for this interview"
        )

    # Convert relative path to absolute path
    absolute_path = FileHandler.get_absolute_path(interview.job_description_path)

    if not FileHandler.file_exists(absolute_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description file not found on disk"
        )

    # Get file extension from the saved file
    file_extension = Path(interview.job_description_path).suffix or '.txt'

    # Return file as download
    return FileResponse(
        path=absolute_path,
        media_type='text/plain',
        filename=f"job_description_interview_{interview_id}{file_extension}"
    )
