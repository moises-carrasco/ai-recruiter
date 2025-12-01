"""
Lookup-related Pydantic schemas.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class LookupItemBase(BaseModel):
    """Base schema for lookup items."""
    domain_id: str
    item_id: str
    text_value: str
    sort_order: Optional[int] = 0
    is_active: Optional[bool] = True


class LookupItemCreate(LookupItemBase):
    """Schema for creating a new lookup item."""
    pass


class LookupItemUpdate(BaseModel):
    """Schema for updating an existing lookup item."""
    domain_id: Optional[str] = None
    item_id: Optional[str] = None
    text_value: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


class LookupItemOut(LookupItemBase):
    """Schema for lookup item output."""
    id: int
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)
