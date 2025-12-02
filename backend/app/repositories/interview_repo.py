"""
Interview repository for database operations.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from .base import BaseRepository
from ..models.interview import Interview, InterviewTranscript, InterviewFeedback


class InterviewRepository(BaseRepository[Interview]):
    """Repository for interview-related database operations."""

    def __init__(self):
        super().__init__(Interview)

    def get_by_link(self, db: Session, interview_link: str) -> Optional[Interview]:
        """Get interview by unique link."""
        return db.query(Interview).filter(Interview.interview_link == interview_link).first()

    def get_by_candidate_id(self, db: Session, candidate_id: int) -> List[Interview]:
        """Get all interviews for a specific candidate."""
        return db.query(Interview).filter(Interview.candidate_id == candidate_id).all()

    def get_by_analyst_id(self, db: Session, analyst_id: int) -> List[Interview]:
        """Get all interviews created by a specific analyst."""
        return db.query(Interview).filter(Interview.analyst_id == analyst_id).all()

    async def filter_by_role_and_client(
        self,
        db: Session,
        role_id: Optional[int] = None,
        client_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Interview]:
        """Filter interviews by role and/or client."""
        query = db.query(Interview)

        if role_id:
            query = query.filter(Interview.role_id == role_id)
        if client_id:
            query = query.filter(Interview.client_id == client_id)

        return query.offset(skip).limit(limit).all()

    def get_by_status(self, db: Session, status_id: int) -> List[Interview]:
        """Get all interviews with a specific status."""
        return db.query(Interview).filter(Interview.status_id == status_id).all()

    def get_scheduled_interviews(
        self,
        db: Session,
        from_datetime: Optional[str] = None,
        to_datetime: Optional[str] = None
    ) -> List[Interview]:
        """Get interviews scheduled within a datetime range."""
        query = db.query(Interview)

        if from_datetime:
            query = query.filter(Interview.scheduled_datetime >= from_datetime)
        if to_datetime:
            query = query.filter(Interview.scheduled_datetime <= to_datetime)

        return query.order_by(Interview.scheduled_datetime).all()

    async def get_interviews_with_filters(
        self,
        db: Session,
        filters: Dict[str, Any],
        skip: int = 0,
        limit: int = 100
    ) -> List[Interview]:
        """Get interviews with complex filtering."""
        query = db.query(Interview)

        # Apply filters
        if filters.get('analyst_id'):
            query = query.filter(Interview.analyst_id == filters['analyst_id'])
        if filters.get('candidate_id'):
            query = query.filter(Interview.candidate_id == filters['candidate_id'])
        if filters.get('role_id'):
            query = query.filter(Interview.role_id == filters['role_id'])
        if filters.get('client_id'):
            query = query.filter(Interview.client_id == filters['client_id'])
        if filters.get('status_id'):
            query = query.filter(Interview.status_id == filters['status_id'])
        if filters.get('scheduled_from'):
            query = query.filter(Interview.scheduled_datetime >= filters['scheduled_from'])
        if filters.get('scheduled_to'):
            query = query.filter(Interview.scheduled_datetime <= filters['scheduled_to'])

        return query.order_by(desc(Interview.created_at)).offset(skip).limit(limit).all()

    async def count_interviews_with_filters(self, db: Session, filters: Dict[str, Any]) -> int:
        """Count interviews with filters."""
        from sqlalchemy import func
        query = db.query(func.count(Interview.id))

        # Apply same filters as get_interviews_with_filters
        if filters.get('analyst_id'):
            query = query.filter(Interview.analyst_id == filters['analyst_id'])
        if filters.get('candidate_id'):
            query = query.filter(Interview.candidate_id == filters['candidate_id'])
        if filters.get('role_id'):
            query = query.filter(Interview.role_id == filters['role_id'])
        if filters.get('client_id'):
            query = query.filter(Interview.client_id == filters['client_id'])
        if filters.get('status_id'):
            query = query.filter(Interview.status_id == filters['status_id'])
        if filters.get('scheduled_from'):
            query = query.filter(Interview.scheduled_datetime >= filters['scheduled_from'])
        if filters.get('scheduled_to'):
            query = query.filter(Interview.scheduled_datetime <= filters['scheduled_to'])

        return query.scalar()

    async def count_total_interviews(self, db: Session) -> int:
        """Count total number of interviews."""
        from sqlalchemy import func
        return db.query(func.count(Interview.id)).scalar()

    async def count_completed_interviews(self, db: Session) -> int:
        """Count completed interviews."""
        from sqlalchemy import func
        # Get completed status ID
        from ..models.lookup import LookupItem
        completed_status = db.query(LookupItem).filter(
            LookupItem.domain_id == 'interview_status',
            LookupItem.item_id == 'completed'
        ).first()

        if not completed_status:
            return 0

        return db.query(func.count(Interview.id)).filter(
            Interview.status_id == completed_status.id
        ).scalar()


class InterviewTranscriptRepository(BaseRepository[InterviewTranscript]):
    """Repository for interview transcript operations."""

    def __init__(self):
        super().__init__(InterviewTranscript)

    def get_by_interview_id(self, db: Session, interview_id: int) -> Optional[InterviewTranscript]:
        """Get transcript for a specific interview."""
        return db.query(InterviewTranscript).filter(
            InterviewTranscript.interview_id == interview_id
        ).first()

    def get_messages_by_interview_id(self, db: Session, interview_id: int) -> List[InterviewTranscript]:
        """Get all messages/transcripts for a specific interview ordered by started_at and id."""
        return db.query(InterviewTranscript).filter(
            InterviewTranscript.interview_id == interview_id
        ).order_by(asc(InterviewTranscript.started_at), asc(InterviewTranscript.id)).all()


class InterviewFeedbackRepository(BaseRepository[InterviewFeedback]):
    """Repository for interview feedback operations."""

    def __init__(self):
        super().__init__(InterviewFeedback)

    def get_by_interview_id(self, db: Session, interview_id: int) -> Optional[InterviewFeedback]:
        """Get feedback for a specific interview."""
        return db.query(InterviewFeedback).filter(
            InterviewFeedback.interview_id == interview_id
        ).first()
