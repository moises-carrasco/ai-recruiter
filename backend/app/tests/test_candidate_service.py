"""
Tests for CandidateService.
"""

import pytest
from app.services.candidate_service import CandidateService
from app.schemas.candidate import CandidateCreate, CandidateUpdate
from fastapi import HTTPException


class TestCandidateService:
    @pytest.mark.asyncio
    async def test_create_candidate(self, db_session):
        """Test candidate creation."""
        service = CandidateService()
        candidate_data = CandidateCreate(
            first_name="Maria",
            last_name="Garcia",
            email="maria.garcia@example.com",
            id_document="12345678"
        )

        candidate = await service.create_candidate(db_session, candidate_data)

        assert candidate.first_name == "Maria"
        assert candidate.last_name == "Garcia"
        assert candidate.email == "maria.garcia@example.com"
        assert candidate.id_document == "12345678"
        assert candidate.is_active is True
        assert candidate.id is not None

    @pytest.mark.asyncio
    async def test_get_candidate_by_id(self, db_session):
        """Test getting candidate by ID."""
        service = CandidateService()
        candidate_data = CandidateCreate(
            first_name="Carlos",
            last_name="Rodriguez",
            email="carlos.rodriguez@example.com",
            id_document="87654321"
        )

        created_candidate = await service.create_candidate(db_session, candidate_data)
        retrieved_candidate = await service.get_candidate_by_id(db_session, created_candidate.id)

        assert retrieved_candidate.id == created_candidate.id
        assert retrieved_candidate.email == "carlos.rodriguez@example.com"

    @pytest.mark.asyncio
    async def test_get_candidate_by_id_not_found(self, db_session):
        """Test getting non-existent candidate raises 404."""
        service = CandidateService()

        with pytest.raises(HTTPException) as exc_info:
            await service.get_candidate_by_id(db_session, 999)

        assert exc_info.value.status_code == 404
        assert "Candidate not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_update_candidate(self, db_session):
        """Test candidate update."""
        service = CandidateService()
        candidate_data = CandidateCreate(
            first_name="Ana",
            last_name="Martinez",
            email="ana.martinez@example.com",
            id_document="11223344"
        )

        created_candidate = await service.create_candidate(db_session, candidate_data)

        update_data = CandidateUpdate(first_name="Ana Updated", email="ana.updated@example.com")
        updated_candidate = await service.update_candidate(db_session, created_candidate.id, update_data)

        assert updated_candidate.first_name == "Ana Updated"
        assert updated_candidate.email == "ana.updated@example.com"
        assert updated_candidate.id_document == "11223344"  # Unchanged

    @pytest.mark.asyncio
    async def test_list_candidates(self, db_session):
        """Test listing candidates."""
        service = CandidateService()

        # Create test candidates
        candidates_data = [
            CandidateCreate(first_name="Test1", last_name="User", email="test1@example.com", id_document="11111111"),
            CandidateCreate(first_name="Test2", last_name="User", email="test2@example.com", id_document="22222222"),
        ]

        for candidate_data in candidates_data:
            await service.create_candidate(db_session, candidate_data)

        # Test listing
        from app.schemas.candidate import CandidateFilter
        filters = CandidateFilter()
        result = await service.list_candidates(db_session, filters)
        assert len(result.candidates) == 2
        assert result.total == 2

    @pytest.mark.asyncio
    async def test_search_candidates_by_name(self, db_session):
        """Test searching candidates by name."""
        service = CandidateService()

        # Create test candidates
        await service.create_candidate(db_session, CandidateCreate(
            first_name="John", last_name="Smith", email="john@example.com", id_document="33333333"
        ))
        await service.create_candidate(db_session, CandidateCreate(
            first_name="Jane", last_name="Smith", email="jane@example.com", id_document="44444444"
        ))

        # Search by last name
        results = await service.search_candidates_by_name(db_session, "Smith", 0, 10)
        assert len(results) == 2

        # Search by first name
        results = await service.search_candidates_by_name(db_session, "John", 0, 10)
        assert len(results) == 1
        assert results[0].first_name == "John"
