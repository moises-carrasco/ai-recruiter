"""
Lookup repository for database operations.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from .base import BaseRepository
from ..models.lookup import LookupItem


class LookupRepository(BaseRepository[LookupItem]):
    """Repository for lookup table operations."""

    def __init__(self):
        super().__init__(LookupItem)

    async def get_by_domain(self, db: Session, domain_id: str) -> List[LookupItem]:
        """Get all lookup items for a specific domain."""
        return db.query(LookupItem).filter(
            LookupItem.domain_id == domain_id
        ).order_by(LookupItem.sort_order, LookupItem.text_value).all()

    async def get_active_items_by_domain(self, db: Session, domain_id: str) -> List[LookupItem]:
        """Get active lookup items for a specific domain."""
        return await self.get_by_domain(db, domain_id)

    async def get_by_domain_and_item_id(self, db: Session, domain_id: str, item_id: str) -> Optional[LookupItem]:
        """Get a specific lookup item by domain and item_id."""
        return db.query(LookupItem).filter(
            LookupItem.domain_id == domain_id,
            LookupItem.item_id == item_id,
            LookupItem.is_active == True
        ).first()

    async def get_all_domains(self, db: Session) -> List[str]:
        """Get all unique domain IDs."""
        from sqlalchemy import distinct
        result = db.query(distinct(LookupItem.domain_id)).all()
        return [row[0] for row in result]

    # Convenience methods for specific domains
    async def get_roles(self, db: Session) -> List[LookupItem]:
        """Get all active roles."""
        return await self.get_by_domain(db, 'roles')

    async def get_clients(self, db: Session) -> List[LookupItem]:
        """Get all active clients."""
        return await self.get_by_domain(db, 'clients')

    async def get_seniorities(self, db: Session) -> List[LookupItem]:
        """Get all active seniorities."""
        return await self.get_by_domain(db, 'seniorities')

    async def get_interview_statuses(self, db: Session) -> List[LookupItem]:
        """Get all active interview statuses."""
        return await self.get_by_domain(db, 'interview_status')
