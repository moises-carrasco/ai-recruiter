"""
User model for system users (administrators and recruiting analysts).
"""

from sqlalchemy import Column, Integer, String, Boolean  # Added Boolean import
from sqlalchemy.sql import func
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    # full_name = Column(String, index=True)
    password_hash = Column(String)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)  # Added is_active attribute
    created_at = Column(String, nullable=False, default=func.datetime('now'))
    updated_at = Column(String, nullable=False, default=func.datetime('now'))

    def __repr__(self):
        return f"<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email})>"
