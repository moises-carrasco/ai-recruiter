"""
Tests for UserService.
"""

import pytest
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate
from fastapi import HTTPException


class TestUserService:
    def test_create_user(self, db_session):
        """Test user creation."""
        service = UserService()
        user_data = UserCreate(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123",
            role="analyst"
        )

        user = service.create_user(db_session, user_data)

        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.role == "analyst"
        assert user.is_active is True
        assert user.id is not None

    def test_get_user_by_id(self, db_session):
        """Test getting user by ID."""
        service = UserService()
        user_data = UserCreate(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            password="password123",
            role="admin"
        )

        created_user = service.create_user(db_session, user_data)
        retrieved_user = service.get_user_by_id(db_session, created_user.id)

        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == "jane.smith@example.com"

    def test_get_user_by_id_not_found(self, db_session):
        """Test getting non-existent user raises 404."""
        service = UserService()

        with pytest.raises(HTTPException) as exc_info:
            service.get_user_by_id(db_session, 999)

        assert exc_info.value.status_code == 404
        assert "User not found" in str(exc_info.value.detail)

    def test_get_user_by_email(self, db_session):
        """Test getting user by email."""
        service = UserService()
        user_data = UserCreate(
            first_name="Bob",
            last_name="Wilson",
            email="bob.wilson@example.com",
            password="password123",
            role="analyst"
        )

        service.create_user(db_session, user_data)
        retrieved_user = service.get_user_by_email(db_session, "bob.wilson@example.com")

        assert retrieved_user.email == "bob.wilson@example.com"
        assert retrieved_user.first_name == "Bob"

    def test_update_user(self, db_session):
        """Test user update."""
        service = UserService()
        user_data = UserCreate(
            first_name="Alice",
            last_name="Brown",
            email="alice.brown@example.com",
            password="password123",
            role="analyst"
        )

        created_user = service.create_user(db_session, user_data)

        update_data = UserUpdate(first_name="Alice Updated", role="admin")
        updated_user = service.update_user(db_session, created_user.id, update_data)

        assert updated_user.first_name == "Alice Updated"
        assert updated_user.role == "admin"
        assert updated_user.email == "alice.brown@example.com"  # Unchanged

    def test_list_users(self, db_session):
        """Test listing users."""
        service = UserService()

        # Create test users
        users_data = [
            UserCreate(first_name="User1", last_name="Test", email="user1@test.com", password="pass", role="analyst"),
            UserCreate(first_name="User2", last_name="Test", email="user2@test.com", password="pass", role="admin"),
        ]

        for user_data in users_data:
            service.create_user(db_session, user_data)

        # Test listing with default filters
        from app.schemas.user import UserFilter
        filters = UserFilter()
        result = service.list_users(db_session, filters)
        assert len(result.users) == 2

        # Test with name filter
        filters = UserFilter(name="User1")
        result = service.list_users(db_session, filters)
        assert len(result.users) == 1
        assert result.users[0].first_name == "User1"
