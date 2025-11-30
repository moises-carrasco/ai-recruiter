"""
User service for user management operations.
"""

from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserOut, UserListResponse
from typing import List  # Added import for List
from app.core.security import get_password_hash
from fastapi import HTTPException, status

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    async def create_user(self, db: Session, user_data: UserCreate) -> UserOut:
        # Hash the password before saving
        user_data.password = get_password_hash(user_data.password)
        return await self.user_repo.create_user(db, user_data)

    async def get_user_by_id(self, db: Session, user_id: int) -> UserOut:
        user = await self.user_repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def get_user_by_email(self, db: Session, email: str) -> UserOut:
        user = await self.user_repo.get_by_email(db, email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def update_user(self, db: Session, user_id: int, user_data: UserUpdate) -> UserOut:
        user = await self.get_user_by_id(db, user_id)
        return await self.user_repo.update_user(db, user, user_data)

    async def delete_user(self, db: Session, user_id: int):
        await self.user_repo.delete_user(db, user_id)

    async def list_users(self, db: Session, filters) -> UserListResponse:
        users = await self.user_repo.list_users(db, filters)
        # Convert SQLAlchemy models to Pydantic schemas
        user_out_list = [UserOut.from_orm(user) for user in users]
        return UserListResponse(users=user_out_list)

    async def search_users_by_name(self, db: Session, name: str, skip: int, limit: int) -> List[UserOut]:
        return await self.user_repo.search_by_name(db, name, skip, limit)
