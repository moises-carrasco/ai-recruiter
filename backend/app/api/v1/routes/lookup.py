"""
Lookup table management routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.services.lookup_service import LookupService
from app.schemas.lookup import LookupItemOut, LookupItemCreate, LookupItemUpdate

router = APIRouter()


def get_lookup_service() -> LookupService:
    """Dependency to get lookup service."""
    return LookupService()


@router.get("/health", status_code=status.HTTP_200_OK)
async def lookup_health():
    """Health check for lookup module."""
    return {"status": "ok", "module": "lookup"}


# Specific endpoints must come before generic ones
@router.get("/roles", response_model=List[LookupItemOut], status_code=status.HTTP_200_OK)
async def get_roles(
    db: Session = Depends(get_db),
    service: LookupService = Depends(get_lookup_service)
):
    """Get all active roles."""
    return await service.get_roles(db)


@router.get("/clients", response_model=List[LookupItemOut], status_code=status.HTTP_200_OK)
async def get_clients(
    db: Session = Depends(get_db),
    service: LookupService = Depends(get_lookup_service)
):
    """Get all active clients."""
    return await service.get_clients(db)


@router.get("/seniorities", response_model=List[LookupItemOut], status_code=status.HTTP_200_OK)
async def get_seniorities(
    db: Session = Depends(get_db),
    service: LookupService = Depends(get_lookup_service)
):
    """Get all active seniorities."""
    return await service.get_seniorities(db)


@router.get("/statuses", response_model=List[LookupItemOut], status_code=status.HTTP_200_OK)
async def get_interview_statuses(
    db: Session = Depends(get_db),
    service: LookupService = Depends(get_lookup_service)
):
    """Get all active interview statuses."""
    return await service.get_interview_statuses(db)


@router.get("/", response_model=List[LookupItemOut], status_code=status.HTTP_200_OK)
async def get_all_lookup_items(
    db: Session = Depends(get_db),
    service: LookupService = Depends(get_lookup_service)
):
    """Get all lookup items."""
    return await service.get_all_lookup_items(db)


@router.get("/{domain_id}", response_model=List[LookupItemOut], status_code=status.HTTP_200_OK)
async def get_lookup_items_by_domain(
    domain_id: str,
    db: Session = Depends(get_db),
    service: LookupService = Depends(get_lookup_service)
):
    """Get lookup items by domain."""
    return await service.get_lookup_items_by_domain(db, domain_id)


@router.post("/", response_model=LookupItemOut, status_code=status.HTTP_201_CREATED)
async def create_lookup_item(
    item_data: LookupItemCreate,
    db: Session = Depends(get_db),
    service: LookupService = Depends(get_lookup_service)
):
    """Create a new lookup item."""
    return await service.create_lookup_item(db, item_data)


@router.put("/{lookup_id}", response_model=LookupItemOut, status_code=status.HTTP_200_OK)
async def update_lookup_item(
    lookup_id: int,
    item_data: LookupItemUpdate,
    db: Session = Depends(get_db),
    service: LookupService = Depends(get_lookup_service)
):
    """Update an existing lookup item."""
    try:
        return await service.update_lookup_item(db, lookup_id, item_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{lookup_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lookup_item(
    lookup_id: int,
    db: Session = Depends(get_db),
    service: LookupService = Depends(get_lookup_service)
):
    """Delete a lookup item."""
    await service.delete_lookup_item(db, lookup_id)
