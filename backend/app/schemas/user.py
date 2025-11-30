"""
User-related Pydantic schemas.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str

class UserListResponse(BaseModel):
    users: List[UserOut]

class UserFilter(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None  # Added is_active filter
    name: Optional[str] = None  # Added name filter for compatibility
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)

    class Config:
        orm_mode = True
