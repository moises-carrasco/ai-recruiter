"""
User repository for database operations.
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status

class UserRepository:
    async def create_user(self, db: Session, user_data: UserCreate):
        user = User(**user_data.dict())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    async def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    async def update_user(self, db: Session, user: User, user_data: UserUpdate):
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
        return user

    async def delete_user(self, db: Session, user_id: int):
        user = await self.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.is_active = False
        await db.commit()

    async def list_users(self, db: Session, filters):
        query = db.query(User)
        if filters.name:
            query = query.filter(User.first_name.contains(filters.name) | User.last_name.contains(filters.name))
        if filters.email:
            query = query.filter(User.email.contains(filters.email))
        if filters.is_active is not None:
            query = query.filter(User.is_active == filters.is_active)
        return query.offset((filters.page - 1) * filters.per_page).limit(filters.per_page).all()

    async def search_by_name(self, db: Session, name: str, skip: int, limit: int):
        return db.query(User).filter(User.first_name.contains(name) | User.last_name.contains(name)).offset(skip).limit(limit).all()
