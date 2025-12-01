"""
Interview-related models: interviews, transcripts, and feedbacks.
"""

from sqlalchemy import Column, Integer, Text, ForeignKey, CheckConstraint, String
from sqlalchemy.sql import func
from .base import Base


class Interview(Base):
    """Interview model for interview configurations and scheduling."""
    __tablename__ = 'interviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    analyst_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('lookup_items.id'), nullable=False)
    seniority_id = Column(Integer, ForeignKey('lookup_items.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('lookup_items.id'))
    cv_file_path = Column(Text)
    job_description_path = Column(Text)
    interview_guidelines = Column(Text)
    scheduled_datetime = Column(Text, nullable=False)
    status_id = Column(Integer, ForeignKey('lookup_items.id'), nullable=False)
    interview_link = Column(Text, unique=True)
    link_expires_at = Column(Text)
    notes = Column(Text)
    created_at = Column(Text, nullable=False, default=func.datetime('now'))
    updated_at = Column(Text, nullable=False, default=func.datetime('now'))

    def __repr__(self):
        return f"<Interview(id={self.id}, candidate_id={self.candidate_id}, scheduled_datetime={self.scheduled_datetime})>"


class InterviewTranscript(Base):
    """Interview transcript model for storing complete interview conversations."""
    __tablename__ = 'interview_transcripts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    interview_id = Column(Integer, ForeignKey('interviews.id', ondelete='CASCADE'), nullable=False)
    transcript_content = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)
    started_at = Column(Text)
    completed_at = Column(Text)
    created_at = Column(Text, nullable=False, default=func.datetime('now'))
    updated_at = Column(Text, nullable=False, default=func.datetime('now'))

    # Add check constraint for role values
    __table_args__ = (
        CheckConstraint("role IN ('candidate', 'assistant', 'system')", name='chk_transcript_role'),
    )

    def __repr__(self):
        return f"<InterviewTranscript(id={self.id}, interview_id={self.interview_id}, role={self.role})>"


class InterviewFeedback(Base):
    """Interview feedback model for AI-generated structured feedback."""
    __tablename__ = 'interview_feedbacks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    interview_id = Column(Integer, ForeignKey('interviews.id', ondelete='CASCADE'), nullable=False)
    general_comments = Column(Text, nullable=False)
    overall_ranking = Column(Integer, nullable=False)
    skills_evaluation = Column(Text, nullable=False)  # JSON structure
    strengths = Column(Text)
    areas_for_improvement = Column(Text)
    job_fit_assessment = Column(Text)
    created_at = Column(Text, nullable=False, default=func.datetime('now'))
    updated_at = Column(Text, nullable=False, default=func.datetime('now'))

    # Add check constraint for ranking values 1-5
    __table_args__ = (
        CheckConstraint('overall_ranking BETWEEN 1 AND 5', name='chk_overall_ranking_range'),
    )

    def __repr__(self):
        return f"<InterviewFeedback(id={self.id}, interview_id={self.interview_id}, overall_ranking={self.overall_ranking})>"
