"""
Tests for AIAgentService.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.ai_agent_service import AIAgentService


class TestAIAgentService:
    def test_init_mock_mode(self):
        """Test initialization in mock mode."""
        service = AIAgentService(mock_mode=True)
        assert service.mock_mode is True

    def test_init_real_mode(self):
        """Test initialization in real mode."""
        service = AIAgentService(mock_mode=False)
        assert service.mock_mode is False

    @pytest.mark.asyncio
    async def test_send_chat_message_mock_mode(self):
        """Test sending chat message in mock mode."""
        service = AIAgentService(mock_mode=True)

        payload = {
            "assistant": "Interviewer_Expert",
            "messages": [{"role": "user", "content": "Hello"}],
            "revision": 3,
            "revisionName": "3"
        }

        response = await service.send_chat_message(payload)

        assert response["success"] is True
        assert response["status"] == "succeeded"
        assert "text" in response
        assert "AI interviewer" in response["text"]
        assert "technical interview" in response["text"]

    @pytest.mark.asyncio
    async def test_send_chat_message_mock_mode_different_payload(self):
        """Test sending chat message in mock mode with different payload."""
        service = AIAgentService(mock_mode=True)

        payload = {
            "assistant": "Interviewer_Expert",
            "messages": [{"role": "user", "content": "Tell me about yourself"}],
            "revision": 1,
            "revisionName": "1"
        }

        response = await service.send_chat_message(payload)

        assert response["success"] is True
        assert response["status"] == "succeeded"
        assert "text" in response
        assert isinstance(response["text"], str)
        assert len(response["text"]) > 0

    def test_ai_service_modes(self):
        """Test that AI service can be initialized in both modes."""
        mock_service = AIAgentService(mock_mode=True)
        real_service = AIAgentService(mock_mode=False)

        assert mock_service.mock_mode is True
        assert real_service.mock_mode is False

    def test_validate_ai_response_valid(self):
        """Test validation of valid AI response."""
        service = AIAgentService()

        valid_response = {
            "success": True,
            "status": "succeeded",
            "requestId": "test-123",
            "text": "Valid response"
        }

        assert service.validate_ai_response(valid_response) is True

    def test_validate_ai_response_invalid_missing_fields(self):
        """Test validation of invalid AI response missing required fields."""
        service = AIAgentService()

        invalid_response = {
            "success": True,
            # Missing status, requestId, text
        }

        assert service.validate_ai_response(invalid_response) is False

    def test_ai_response_structure(self):
        """Test that AI responses have the expected structure."""
        service = AIAgentService(mock_mode=True)

        # Test that the service has the expected methods
        assert hasattr(service, 'send_chat_message')
        assert hasattr(service, 'validate_ai_response')
        assert service.mock_mode is True
