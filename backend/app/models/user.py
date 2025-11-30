"""
User model for system users (administrators and recruiting analysts).
"""

from sqlalchemy import Column, Integer, String, Boolean  # Added Boolean import
from backend.app.models.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)  # Added is_active attribute

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
