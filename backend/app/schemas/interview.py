"""
Interview-related Pydantic schemas.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


class InterviewCreate(BaseModel):
    """Schema for creating a new interview."""
    analyst_id: int
    candidate_id: int
    role_id: int
    seniority_id: int
    client_id: int  # Made mandatory
    cv_file_path: Optional[str] = None
    job_description_path: Optional[str] = None
    interview_guidelines: Optional[str] = None
    scheduled_datetime: str  # ISO8601 format
    status_id: int
    notes: Optional[str] = None


class InterviewUpdate(BaseModel):
    """Schema for updating an existing interview."""
    analyst_id: Optional[int] = None
    candidate_id: Optional[int] = None
    role_id: Optional[int] = None
    seniority_id: Optional[int] = None
    client_id: Optional[int] = None
    cv_file_path: Optional[str] = None
    job_description_path: Optional[str] = None
    interview_guidelines: Optional[str] = None
    scheduled_datetime: Optional[str] = None
    status_id: Optional[int] = None
    notes: Optional[str] = None


class InterviewOut(BaseModel):
    """Schema for interview output with related data."""
    id: int
    analyst_id: int
    candidate_id: int
    role_id: int
    seniority_id: int
    client_id: Optional[int] = None
    cv_file_path: Optional[str] = None
    job_description_path: Optional[str] = None
    interview_guidelines: Optional[str] = None
    scheduled_datetime: str
    status_id: int
    interview_link: Optional[str] = None
    link_expires_at: Optional[str] = None
    notes: Optional[str] = None
    created_at: str
    updated_at: str

    # Related data
    analyst_name: Optional[str] = None
    candidate_name: Optional[str] = None
    role_text: Optional[str] = None
    seniority_text: Optional[str] = None
    client_text: Optional[str] = None
    status_text: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class InterviewListResponse(BaseModel):
    """Schema for paginated interview list response."""
    interviews: List[InterviewOut]
    total: int
    page: int
    per_page: int
    total_pages: int


class InterviewFilter(BaseModel):
    """Schema for filtering interviews."""
    analyst_id: Optional[int] = None
    candidate_id: Optional[int] = None
    role_id: Optional[int] = None
    client_id: Optional[int] = None
    status_id: Optional[int] = None
    scheduled_from: Optional[str] = None  # ISO8601 format
    scheduled_to: Optional[str] = None    # ISO8601 format
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)


class InterviewLinkAccess(BaseModel):
    """Schema for accessing interview via link."""
    interview_link: str


class InterviewStartRequest(BaseModel):
    """Schema for starting an interview."""
    pass  # No additional data needed


class InterviewCompleteRequest(BaseModel):
    """Schema for completing an interview."""
    transcript_content: str


class ChatMessageRequest(BaseModel):
    """Schema for sending chat messages during interview."""
    message: str


class InterviewTranscriptOut(BaseModel):
    """Schema for interview transcript output."""
    id: int
    interview_id: int
    transcript_content: str
    role: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class InterviewTranscriptsList(BaseModel):
    """Schema for list of interview transcripts."""
    transcripts: List[InterviewTranscriptOut]

    model_config = ConfigDict(from_attributes=True)


class SkillEvaluation(BaseModel):
    """Schema for individual skill evaluation."""
    skill_name: str
    ranking: int = Field(ge=1, le=5)
    comments: str


class InterviewFeedbackOut(BaseModel):
    """Schema for interview feedback output."""
    id: int
    interview_id: int
    general_comments: str
    overall_ranking: int = Field(ge=1, le=5)
    skills_evaluation: List[SkillEvaluation]
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    job_fit_assessment: Optional[str] = None
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class InterviewWithFeedbackOut(InterviewOut):
    """Schema for interview with associated feedback."""
    feedback: Optional[InterviewFeedbackOut] = None
    transcript: Optional[InterviewTranscriptOut] = None


# File upload schemas
class FileUploadResponse(BaseModel):
    """Schema for file upload response."""
    file_path: str
    filename: str
    content_type: str
    size: int
