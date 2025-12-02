"""
Tests for users API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.schemas.user import UserCreate, UserUpdate


class TestUsersAPI:
    def test_create_user(self, client: TestClient):
        """Test creating a user via API."""
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "password": "password123",
            "role": "analyst"
        }

        response = client.post("/api/v1/users/", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"
        assert data["email"] == "test.user@example.com"
        assert data["role"] == "analyst"
        assert data["is_active"] is True
        assert "id" in data

    def test_get_user_by_id(self, client: TestClient):
        """Test getting a user by ID via API."""
        # First create a user
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "password123",
            "role": "admin"
        }

        create_response = client.post("/api/v1/users/", json=user_data)
        assert create_response.status_code == 201
        user_id = create_response.json()["id"]

        # Now get the user
        response = client.get(f"/api/v1/users/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == "jane.doe@example.com"

    def test_get_user_by_id_not_found(self, client: TestClient):
        """Test getting a non-existent user returns 404."""
        response = client.get("/api/v1/users/999")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "User not found" in data["detail"]

    def test_get_users_list(self, client: TestClient):
        """Test getting list of users via API."""
        # Create test users
        users_data = [
            {
                "first_name": "User1",
                "last_name": "Test",
                "email": "user1@test.com",
                "password": "pass",
                "role": "analyst"
            },
            {
                "first_name": "User2",
                "last_name": "Test",
                "email": "user2@test.com",
                "password": "pass",
                "role": "admin"
            }
        ]

        for user_data in users_data:
            response = client.post("/api/v1/users/", json=user_data)
            assert response.status_code == 201

        # Get users list
        response = client.get("/api/v1/users/")

        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert len(data["users"]) >= 2  # At least the ones we created

    def test_update_user(self, client: TestClient):
        """Test updating a user via API."""
        # Create a user
        user_data = {
            "first_name": "Original",
            "last_name": "Name",
            "email": "original@example.com",
            "password": "password123",
            "role": "analyst"
        }

        create_response = client.post("/api/v1/users/", json=user_data)
        assert create_response.status_code == 201
        user_id = create_response.json()["id"]

        # Update the user
        update_data = {
            "first_name": "Updated",
            "role": "admin"
        }

        response = client.put(f"/api/v1/users/{user_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["role"] == "admin"
        assert data["last_name"] == "Name"  # Unchanged

    def test_delete_user(self, client: TestClient):
        """Test deleting a user via API."""
        # Create a user
        user_data = {
            "first_name": "To",
            "last_name": "Delete",
            "email": "delete@example.com",
            "password": "password123",
            "role": "analyst"
        }

        create_response = client.post("/api/v1/users/", json=user_data)
        assert create_response.status_code == 201
        user_id = create_response.json()["id"]

        # Delete the user
        response = client.delete(f"/api/v1/users/{user_id}")

        assert response.status_code == 204

        # Verify user is deleted (soft delete - should still exist but inactive)
        get_response = client.get(f"/api/v1/users/{user_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["is_active"] is False

    def test_search_users_by_name(self, client: TestClient):
        """Test searching users by name via API."""
        # Create test users
        users_data = [
            {
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@test.com",
                "password": "pass",
                "role": "analyst"
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@test.com",
                "password": "pass",
                "role": "analyst"
            }
        ]

        for user_data in users_data:
            response = client.post("/api/v1/users/", json=user_data)
            assert response.status_code == 201

        # Search by name
        response = client.get("/api/v1/users/search/by-name?name=Smith")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Search by first name
        response = client.get("/api/v1/users/search/by-name?name=John")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["first_name"] == "John"
