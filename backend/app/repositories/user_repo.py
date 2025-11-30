"""
User repository for database operations.
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException, status

class UserRepository:
    def create_user(self, db: Session, user_data: UserCreate):
        # Convert UserCreate to dict and map password to password_hash
        user_dict = user_data.dict()
        user_dict['password_hash'] = user_dict.pop('password')
        user = User(**user_dict)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def update_user(self, db: Session, user: User, user_data: UserUpdate):
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, db: Session, user_id: int):
        user = self.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.is_active = False
        db.commit()

    def list_users(self, db: Session, filters):
        query = db.query(User)
        if filters.name:
            query = query.filter(User.first_name.contains(filters.name) | User.last_name.contains(filters.name))
        if filters.email:
            query = query.filter(User.email.contains(filters.email))
        if filters.is_active is not None:
            query = query.filter(User.is_active == filters.is_active)
        return query.offset((filters.page - 1) * filters.per_page).limit(filters.per_page).all()

    def search_by_name(self, db: Session, name: str, skip: int, limit: int):
        return db.query(User).filter(User.first_name.contains(name) | User.last_name.contains(name)).offset(skip).limit(limit).all()
