"""
Lookup model for generic lookup table (roles, clients, seniorities, statuses).
"""

from sqlalchemy import Column, Integer, Text, UniqueConstraint
from sqlalchemy.sql import func
from .base import Base


class LookupItem(Base):
    """Generic lookup table for roles, clients, seniorities, and statuses."""
    __tablename__ = 'lookup_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain_id = Column(Text, nullable=False)
    item_id = Column(Text, nullable=False)
    text_value = Column(Text, nullable=False)
    is_active = Column(Integer, nullable=False, default=1)
    sort_order = Column(Integer, default=0)
    created_at = Column(Text, nullable=False, default=func.datetime('now'))
    updated_at = Column(Text, nullable=False, default=func.datetime('now'))

    # Unique constraint on domain_id + item_id
    __table_args__ = (
        UniqueConstraint('domain_id', 'item_id', name='unq_lookup_domain_item'),
    )

    def __repr__(self):
        return f"<LookupItem(id={self.id}, domain='{self.domain_id}', item='{self.item_id}', text='{self.text_value}')>"
