"""
User management routes.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserOut, UserListResponse, UserFilter

router = APIRouter()


def get_user_service() -> UserService:
    """Dependency to get user service."""
    return UserService()


@router.get("/", response_model=UserListResponse, status_code=status.HTTP_200_OK)
async def get_users(
    name: Optional[str] = Query(None, description="Filter by user name"),
    email: Optional[str] = Query(None, description="Filter by user email"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    """
    Get list of users with filtering and pagination.
    
    - **name**: Filter users by name (partial match)
    - **email**: Filter users by email (partial match)
    - **is_active**: Filter by active status (default: True)
    - **page**: Page number for pagination (default: 1)
    - **per_page**: Number of items per page (default: 20, max: 100)
    """
    filters = UserFilter(
        name=name,
        email=email,
        is_active=is_active,
        page=page,
        per_page=per_page
    )
    return await service.list_users(db, filters)


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    """
    Create a new user.
    
    - **first_name**: User's first name (required)
    - **last_name**: User's last name (required)
    - **email**: User's email address (required, must be unique)
    - **last_name**: User's last name (required)
    - **first_name**: User's first name (required)
    """
    return await service.create_user(db, user_data)


@router.get("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    """
    Get a specific user by ID.
    
    - **user_id**: The ID of the user to retrieve
    """
    return await service.get_user_by_id(db, user_id)


@router.put("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    """
    Update an existing user.
    
    - **user_id**: The ID of the user to update
    - **first_name**: Updated first name (optional)
    - **last_name**: Updated last name (optional)
    - **email**: Updated email address (optional, must be unique)
    - **role**: Updated role (optional)
    - **is_active**: Updated active status (optional)
    """
    return await service.update_user(db, user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    """
    Soft delete a user (sets is_active to False).
    
    - **user_id**: The ID of the user to delete
    """
    await service.delete_user(db, user_id)


@router.get("/search/by-name", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def search_users_by_name(
    name: str = Query(..., min_length=1, description="Name to search for"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    """
    Search users by name.
    
    - **name**: Name to search for (partial match on first_name, last_name, or full name)
    - **skip**: Number of records to skip for pagination (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 100)
    """
    return await service.search_users_by_name(db, name, skip, limit)
