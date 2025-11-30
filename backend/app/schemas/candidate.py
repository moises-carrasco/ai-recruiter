"""
Candidate-related Pydantic schemas.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class CandidateBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    id_document: str = Field(..., min_length=1, max_length=50)


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    id_document: Optional[str] = Field(None, min_length=1, max_length=50)
    is_active: Optional[bool] = None


class CandidateOut(CandidateBase):
    id: int
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class CandidateListResponse(BaseModel):
    candidates: list[CandidateOut]
    total: int
    page: int
    per_page: int
    total_pages: int


class CandidateFilter(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = True
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
