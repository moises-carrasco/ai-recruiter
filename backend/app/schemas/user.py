"""
User-related Pydantic schemas.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: str

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    users: List[UserOut]

class UserFilter(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None  # Added is_active filter
    name: Optional[str] = None  # Added name filter for compatibility
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
