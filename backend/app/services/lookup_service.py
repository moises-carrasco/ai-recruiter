"""
Lookup service for managing lookup table data.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.lookup_repo import LookupRepository
from ..schemas.lookup import LookupItemOut, LookupItemCreate, LookupItemUpdate


class LookupService:
    """Service for lookup table operations."""

    def __init__(self):
        self.lookup_repo = LookupRepository()

    async def get_lookup_item_by_id(self, db: Session, lookup_id: int) -> Optional[LookupItemOut]:
        """Get a lookup item by ID."""
        item = await self.lookup_repo.get_by_id(db, lookup_id)
        if item:
            return LookupItemOut.model_validate(item)
        return None

    async def get_lookup_items_by_domain(self, db: Session, domain_id: str) -> List[LookupItemOut]:
        """Get all lookup items for a specific domain."""
        items = await self.lookup_repo.get_by_domain(db, domain_id)
        return [LookupItemOut.model_validate(item) for item in items]

    async def get_all_lookup_items(self, db: Session) -> List[LookupItemOut]:
        """Get all lookup items."""
        items = await self.lookup_repo.get_all(db)
        return [LookupItemOut.model_validate(item) for item in items]

    async def get_roles(self, db: Session) -> List[LookupItemOut]:
        """Get all active roles."""
        items = await self.lookup_repo.get_roles(db)
        return [LookupItemOut.model_validate(item) for item in items]

    async def get_clients(self, db: Session) -> List[LookupItemOut]:
        """Get all active clients."""
        items = await self.lookup_repo.get_clients(db)
        return [LookupItemOut.model_validate(item) for item in items]

    async def get_seniorities(self, db: Session) -> List[LookupItemOut]:
        """Get all active seniorities."""
        items = await self.lookup_repo.get_seniorities(db)
        return [LookupItemOut.model_validate(item) for item in items]

    async def get_interview_statuses(self, db: Session) -> List[LookupItemOut]:
        """Get all active interview statuses."""
        items = await self.lookup_repo.get_interview_statuses(db)
        return [LookupItemOut.model_validate(item) for item in items]

    async def create_lookup_item(self, db: Session, item_data: LookupItemCreate) -> LookupItemOut:
        """Create a new lookup item."""
        item_dict = item_data.model_dump()
        item = await self.lookup_repo.create(db, item_dict)
        return LookupItemOut.model_validate(item)

    async def update_lookup_item(self, db: Session, lookup_id: int, item_data: LookupItemUpdate) -> LookupItemOut:
        """Update an existing lookup item."""
        item = await self.lookup_repo.get_by_id(db, lookup_id)
        if not item:
            raise ValueError("Lookup item not found")

        update_dict = item_data.model_dump(exclude_unset=True)
        updated_item = await self.lookup_repo.update(db, item, update_dict)
        return LookupItemOut.model_validate(updated_item)

    async def delete_lookup_item(self, db: Session, lookup_id: int) -> None:
        """Delete a lookup item (soft delete)."""
        await self.lookup_repo.soft_delete(db, lookup_id)

    async def get_all_domains(self, db: Session) -> List[str]:
        """Get all unique domain IDs."""
        return await self.lookup_repo.get_all_domains(db)
