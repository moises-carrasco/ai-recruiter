"""
Candidate management routes.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.candidate_service import CandidateService
from app.schemas.candidate import (
    CandidateCreate,
    CandidateUpdate,
    CandidateOut,
    CandidateListResponse,
    CandidateFilter
)

router = APIRouter()


def get_candidate_service() -> CandidateService:
    """Dependency to get candidate service."""
    return CandidateService()


@router.get("/", response_model=CandidateListResponse, status_code=status.HTTP_200_OK)
async def get_candidates(
    name: Optional[str] = Query(None, description="Filter by candidate name"),
    email: Optional[str] = Query(None, description="Filter by candidate email"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    service: CandidateService = Depends(get_candidate_service)
):
    """
    Get list of candidates with filtering and pagination.
    
    - **name**: Filter candidates by name (partial match)
    - **email**: Filter candidates by email (partial match)
    - **is_active**: Filter by active status (default: True)
    - **page**: Page number for pagination (default: 1)
    - **per_page**: Number of items per page (default: 20, max: 100)
    """
    filters = CandidateFilter(
        name=name,
        email=email,
        is_active=is_active,
        page=page,
        per_page=per_page
    )
    return await service.list_candidates(db, filters)


@router.post("/", response_model=CandidateOut, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    candidate_data: CandidateCreate,
    db: Session = Depends(get_db),
    service: CandidateService = Depends(get_candidate_service)
):
    """
    Create a new candidate.
    
    - **first_name**: Candidate's first name (required)
    - **last_name**: Candidate's last name (required)
    - **email**: Candidate's email address (required, must be unique)
    - **id_document**: Candidate's ID document (required, must be unique)
    """
    return await service.create_candidate(db, candidate_data)


@router.get("/{candidate_id}", response_model=CandidateOut, status_code=status.HTTP_200_OK)
async def get_candidate_by_id(
    candidate_id: int,
    db: Session = Depends(get_db),
    service: CandidateService = Depends(get_candidate_service)
):
    """
    Get a specific candidate by ID.
    
    - **candidate_id**: The ID of the candidate to retrieve
    """
    return await service.get_candidate_by_id(db, candidate_id)


@router.put("/{candidate_id}", response_model=CandidateOut, status_code=status.HTTP_200_OK)
async def update_candidate(
    candidate_id: int,
    candidate_data: CandidateUpdate,
    db: Session = Depends(get_db),
    service: CandidateService = Depends(get_candidate_service)
):
    """
    Update an existing candidate.
    
    - **candidate_id**: The ID of the candidate to update
    - **first_name**: Updated first name (optional)
    - **last_name**: Updated last name (optional)
    - **email**: Updated email address (optional, must be unique)
    - **id_document**: Updated ID document (optional, must be unique)
    - **is_active**: Updated active status (optional)
    """
    return await service.update_candidate(db, candidate_id, candidate_data)


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    service: CandidateService = Depends(get_candidate_service)
):
    """
    Soft delete a candidate (sets is_active to False).
    
    - **candidate_id**: The ID of the candidate to delete
    """
    await service.delete_candidate(db, candidate_id)


@router.get("/search/by-name", response_model=List[CandidateOut], status_code=status.HTTP_200_OK)
async def search_candidates_by_name(
    name: str = Query(..., min_length=1, description="Name to search for"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    service: CandidateService = Depends(get_candidate_service)
):
    """
    Search candidates by name.
    
    - **name**: Name to search for (partial match on first_name, last_name, or full name)
    - **skip**: Number of records to skip for pagination (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 100)
    """
    return await service.search_candidates_by_name(db, name, skip, limit)


@router.get("/email/{email}", response_model=CandidateOut, status_code=status.HTTP_200_OK)
async def get_candidate_by_email(
    email: str,
    db: Session = Depends(get_db),
    service: CandidateService = Depends(get_candidate_service)
):
    """
    Get a candidate by email address.
    
    - **email**: The email address of the candidate to retrieve
    """
    return await service.get_candidate_by_email(db, email)
