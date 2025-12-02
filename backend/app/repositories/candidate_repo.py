"""
Candidate repository for database operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from .base import BaseRepository
from ..models.candidate import Candidate


class CandidateRepository(BaseRepository[Candidate]):
    def __init__(self):
        super().__init__(Candidate)

    async def get_by_email(self, db: Session, email: str) -> Optional[Candidate]:
        """Get candidate by email address."""
        return db.query(self.model).filter(self.model.email == email).first()

    async def get_by_id_document(self, db: Session, id_document: str) -> Optional[Candidate]:
        """Get candidate by ID document."""
        return db.query(self.model).filter(self.model.id_document == id_document).first()

    async def search_by_name(
        self,
        db: Session,
        name: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Candidate]:
        """Search candidates by name (first_name or last_name)."""
        search_term = f"%{name}%"
        return (
            db.query(self.model)
            .filter(
                or_(
                    self.model.first_name.ilike(search_term),
                    self.model.last_name.ilike(search_term),
                    func.concat(self.model.first_name, ' ', self.model.last_name).ilike(search_term)
                )
            )
            .order_by(self.model.first_name, self.model.last_name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def get_active_candidates(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Candidate]:
        """Get all active candidates."""
        return (
            db.query(self.model)
            .filter(self.model.is_active == 1)
            .order_by(self.model.first_name, self.model.last_name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def get_filtered_candidates(
        self,
        db: Session,
        name: Optional[str] = None,
        email: Optional[str] = None,
        is_active: Optional[bool] = True,
        skip: int = 0,
        limit: int = 100
    ) -> List[Candidate]:
        """Get candidates with multiple filters."""
        query = db.query(self.model)

        # Apply filters
        if is_active is not None:
            query = query.filter(self.model.is_active == (1 if is_active else 0))

        if name:
            search_term = f"%{name}%"
            query = query.filter(
                or_(
                    self.model.first_name.ilike(search_term),
                    self.model.last_name.ilike(search_term),
                    func.concat(self.model.first_name, ' ', self.model.last_name).ilike(search_term)
                )
            )

        if email:
            email_term = f"%{email}%"
            query = query.filter(self.model.email.ilike(email_term))

        return query.order_by(self.model.first_name, self.model.last_name)\
            .offset(skip).limit(limit).all()

    async def count_filtered_candidates(
        self,
        db: Session,
        name: Optional[str] = None,
        email: Optional[str] = None,
        is_active: Optional[bool] = True
    ) -> int:
        """Count candidates with filters."""
        query = db.query(func.count(self.model.id))

        # Apply same filters as get_filtered_candidates
        if is_active is not None:
            query = query.filter(self.model.is_active == (1 if is_active else 0))

        if name:
            search_term = f"%{name}%"
            query = query.filter(
                or_(
                    self.model.first_name.ilike(search_term),
                    self.model.last_name.ilike(search_term),
                    func.concat(self.model.first_name, ' ', self.model.last_name).ilike(search_term)
                )
            )

        if email:
            email_term = f"%{email}%"
            query = query.filter(self.model.email.ilike(email_term))

        return query.scalar()

    async def check_email_exists(self, db: Session, email: str, exclude_id: Optional[int] = None) -> bool:
        """Check if email already exists, optionally excluding a specific ID."""
        query = db.query(self.model).filter(
            self.model.email == email,
            self.model.is_active == 1
        )
        if exclude_id:
            query = query.filter(self.model.id != exclude_id)
        return query.first() is not None

    async def count_active_candidates(self, db: Session) -> int:
        """Count total number of active candidates."""
        from sqlalchemy import func
        return db.query(func.count(self.model.id)).filter(
            self.model.is_active == 1
        ).scalar()

    async def check_id_document_exists(self, db: Session, id_document: str, exclude_id: Optional[int] = None) -> bool:
        """Check if ID document already exists, optionally excluding a specific ID."""
        query = db.query(self.model).filter(
            self.model.id_document == id_document,
            self.model.is_active == 1
        )
        if exclude_id:
            query = query.filter(self.model.id != exclude_id)
        return query.first() is not None
