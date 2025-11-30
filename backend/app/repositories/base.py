"""
Base repository class with common CRUD operations.
"""

from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from sqlalchemy.sql import func

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    async def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination."""
        return db.query(self.model).offset(skip).limit(limit).all()

    async def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """Get multiple records with optional filters."""
        query = db.query(self.model)
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.filter(getattr(self.model, key) == value)
        
        return query.offset(skip).limit(limit).all()

    async def count(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records with optional filters."""
        query = db.query(func.count(self.model.id))
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.filter(getattr(self.model, key) == value)
        
        return query.scalar()

    async def create(self, db: Session, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new record."""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(
        self, 
        db: Session, 
        db_obj: ModelType, 
        obj_in: Dict[str, Any]
    ) -> ModelType:
        """Update an existing record."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def delete(self, db: Session, id: int) -> Optional[ModelType]:
        """Delete a record by ID."""
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    async def soft_delete(self, db: Session, id: int) -> Optional[ModelType]:
        """Soft delete a record by setting is_active to 0."""
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj and hasattr(obj, 'is_active'):
            obj.is_active = 0
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj
