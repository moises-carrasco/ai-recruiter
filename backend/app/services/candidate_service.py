"""
Candidate service for candidate management operations.
"""

import logging
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..repositories.candidate_repo import CandidateRepository
from ..schemas.candidate import CandidateCreate, CandidateUpdate, CandidateOut, CandidateListResponse, CandidateFilter
from ..models.candidate import Candidate
import math

logger = logging.getLogger(__name__)


class CandidateService:
    def __init__(self):
        self.repository = CandidateRepository()

    async def create_candidate(self, db: Session, candidate_data: CandidateCreate) -> CandidateOut:
        """Create a new candidate."""
        logger.info(f"Creating candidate with email: {candidate_data.email}")
        
        # Check if email already exists
        if await self.repository.check_email_exists(db, candidate_data.email):
            logger.warning(f"Attempt to create candidate with existing email: {candidate_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if ID document already exists
        if await self.repository.check_id_document_exists(db, candidate_data.id_document):
            logger.warning(f"Attempt to create candidate with existing ID document: {candidate_data.id_document}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID document already registered"
            )
        
        try:
            # Create candidate
            candidate_dict = candidate_data.model_dump()
            candidate_dict['is_active'] = 1
            
            db_candidate = await self.repository.create(db, candidate_dict)
            logger.info(f"Successfully created candidate with ID: {db_candidate.id}")
            
            return CandidateOut.model_validate(db_candidate)
        
        except Exception as e:
            logger.error(f"Error creating candidate: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating candidate"
            )

    async def get_candidate_by_id(self, db: Session, candidate_id: int) -> CandidateOut:
        """Get candidate by ID."""
        logger.info(f"Retrieving candidate with ID: {candidate_id}")
        
        candidate = await self.repository.get_by_id(db, candidate_id)
        if not candidate:
            logger.warning(f"Candidate not found with ID: {candidate_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found"
            )
        
        return CandidateOut.model_validate(candidate)

    async def get_candidate_by_email(self, db: Session, email: str) -> CandidateOut:
        """Get candidate by email."""
        logger.info(f"Retrieving candidate with email: {email}")
        
        candidate = await self.repository.get_by_email(db, email)
        if not candidate:
            logger.warning(f"Candidate not found with email: {email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found"
            )
        
        return CandidateOut.model_validate(candidate)

    async def update_candidate(
        self, 
        db: Session, 
        candidate_id: int, 
        candidate_data: CandidateUpdate
    ) -> CandidateOut:
        """Update an existing candidate."""
        logger.info(f"Updating candidate with ID: {candidate_id}")
        
        # Get existing candidate
        db_candidate = await self.repository.get_by_id(db, candidate_id)
        if not db_candidate:
            logger.warning(f"Candidate not found for update with ID: {candidate_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found"
            )
        
        # Check email uniqueness if email is being updated
        if candidate_data.email and candidate_data.email != db_candidate.email:
            if await self.repository.check_email_exists(db, candidate_data.email, exclude_id=candidate_id):
                logger.warning(f"Attempt to update candidate with existing email: {candidate_data.email}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Check ID document uniqueness if ID document is being updated
        if candidate_data.id_document and candidate_data.id_document != db_candidate.id_document:
            if await self.repository.check_id_document_exists(db, candidate_data.id_document, exclude_id=candidate_id):
                logger.warning(f"Attempt to update candidate with existing ID document: {candidate_data.id_document}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID document already registered"
                )
        
        try:
            # Update candidate
            update_data = candidate_data.model_dump(exclude_unset=True)
            if 'is_active' in update_data:
                update_data['is_active'] = 1 if update_data['is_active'] else 0
            
            updated_candidate = await self.repository.update(db, db_candidate, update_data)
            logger.info(f"Successfully updated candidate with ID: {candidate_id}")
            
            return CandidateOut.model_validate(updated_candidate)
        
        except Exception as e:
            logger.error(f"Error updating candidate: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating candidate"
            )

    async def delete_candidate(self, db: Session, candidate_id: int) -> bool:
        """Soft delete a candidate."""
        logger.info(f"Soft deleting candidate with ID: {candidate_id}")
        
        candidate = await self.repository.get_by_id(db, candidate_id)
        if not candidate:
            logger.warning(f"Candidate not found for deletion with ID: {candidate_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidate not found"
            )
        
        try:
            await self.repository.soft_delete(db, candidate_id)
            logger.info(f"Successfully soft deleted candidate with ID: {candidate_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting candidate: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting candidate"
            )

    async def list_candidates(self, db: Session, filters: CandidateFilter) -> CandidateListResponse:
        """List candidates with filtering and pagination."""
        logger.info(f"Listing candidates with filters: {filters.model_dump()}")
        
        try:
            # Calculate pagination
            skip = (filters.page - 1) * filters.per_page
            
            # Default to showing active candidates only if not specified
            if filters.is_active is None:
                filters.is_active = True
            
            # Get filtered candidates
            candidates = await self.repository.get_filtered_candidates(
                db=db,
                name=filters.name,
                email=filters.email,
                is_active=filters.is_active,
                skip=skip,
                limit=filters.per_page
            )
            
            # Get total count
            total = await self.repository.count_filtered_candidates(
                db=db,
                name=filters.name,
                email=filters.email,
                is_active=filters.is_active
            )
            
            # Calculate total pages
            total_pages = math.ceil(total / filters.per_page) if total > 0 else 1
            
            # Convert to output schema
            candidate_list = [CandidateOut.model_validate(candidate) for candidate in candidates]
            
            logger.info(f"Successfully retrieved {len(candidate_list)} candidates (total: {total})")
            
            return CandidateListResponse(
                candidates=candidate_list,
                total=total,
                page=filters.page,
                per_page=filters.per_page,
                total_pages=total_pages
            )
        
        except Exception as e:
            logger.error(f"Error listing candidates: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving candidates"
            )

    async def search_candidates_by_name(
        self, 
        db: Session, 
        name: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[CandidateOut]:
        """Search candidates by name."""
        logger.info(f"Searching candidates by name: {name}")
        
        try:
            candidates = await self.repository.search_by_name(db, name, skip, limit)
            candidate_list = [CandidateOut.model_validate(candidate) for candidate in candidates]
            
            logger.info(f"Found {len(candidate_list)} candidates matching name: {name}")
            return candidate_list
        
        except Exception as e:
            logger.error(f"Error searching candidates by name: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error searching candidates"
            )
