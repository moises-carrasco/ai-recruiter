"""
Candidate model for interview candidates.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from .base import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    id_document = Column(String, nullable=False, unique=True)
    is_active = Column(Integer, nullable=False, default=1)
    created_at = Column(String, nullable=False, default=func.datetime('now'))
    updated_at = Column(String, nullable=False, default=func.datetime('now'))

    def __repr__(self):
        return f"<Candidate(id={self.id}, email='{self.email}', name='{self.first_name} {self.last_name}')>"
