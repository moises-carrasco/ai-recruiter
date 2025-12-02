"""
AI Agent service for conducting technical interviews.
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from app.core.config import settings

# Optional import for real API calls
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

logger = logging.getLogger(__name__)


class AIAgentService:
    """Service for interacting with the external AI assistant API."""

    def __init__(self, mock_mode: bool = False):
        self.api_url = settings.AI_API_URL
        self.auth_token = settings.AI_API_KEY
        self.mock_mode = mock_mode

    async def send_chat_message(self, conversation_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send conversation payload to AI assistant and return response.
        """
        if self.mock_mode:
            logger.info("Using mock mode for AI assistant")
            # Simulate processing delay
            import asyncio
            await asyncio.sleep(0.5)

            mock_text = self._generate_mock_ai_response(conversation_payload)
            mock_response = {
                "progress": 100,
                "providerName": "mock_openai",
                "providerResponse": json.dumps({
                    "created": int(datetime.utcnow().timestamp()),
                    "usage": {
                        "completion_tokens": 150,
                        "prompt_tokens": 200,
                        "total_cost": 0.00015,
                        "completion_tokens_details": {"reasoning_tokens": 100},
                        "prompt_tokens_details": {"cached_tokens": 0},
                        "total_tokens": 350,
                        "currency": "USD",
                        "completion_cost": 0.00012,
                        "prompt_cost": 0.00003
                    },
                    "model": "mock-gpt-5-nano-2025-08-07",
                    "service_tier": "default",
                    "id": f"mock-chatcmpl-{datetime.utcnow().isoformat()}",
                    "choices": [{
                        "finish_reason": "stop",
                        "provider_specific_fields": {},
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "annotations": [],
                            "content": mock_text
                        }
                    }],
                    "object": "chat.completion"
                }),
                "requestId": f"mock-{datetime.utcnow().isoformat()}",
                "status": "succeeded",
                "success": True,
                "text": mock_text
            }

            logger.info(f"AI service mock response: status={mock_response['status']}, success={mock_response['success']}")
            return mock_response
        else:
            logger.info("Sending real chat message to AI assistant")
            response = await self._send_real_api_request(conversation_payload)

            logger.info(f"AI service response: status={response.get('status')}, success={response.get('success')}")
            return response

    def _generate_mock_ai_response(self, conversation_payload: Dict[str, Any]) -> str:
        """Generate a mock AI response based on conversation context."""
        messages = conversation_payload.get('messages', [])

        # Add timestamp for uniqueness
        timestamp = datetime.utcnow().strftime("%H:%M:%S")

        # Check if this is the first message (kickoff)
        if len(messages) <= 1:
            return f"Hello! I'm your AI interviewer. I'm excited to conduct this technical interview with you. To get started, could you please tell me a bit about your background and experience in this field?\n\n*(Response generated at {timestamp})*"

        # Get the last user message
        last_user_message = None
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                last_user_message = msg.get('content', '').lower()
                break

        # Generate contextual responses based on common interview topics
        if 'experience' in last_user_message or 'background' in last_user_message:
            return f"Thank you for sharing your background. That's impressive experience! Let's dive into some technical questions. Can you walk me through a challenging project you've worked on and the technical decisions you made?\n\n*(Response generated at {timestamp})*"

        elif 'project' in last_user_message or 'worked on' in last_user_message:
            return f"That sounds like a complex and interesting project. How did you handle version control and collaboration with your team? What tools or methodologies did you use?\n\n*(Response generated at {timestamp})*"

        elif 'version control' in last_user_message or 'git' in last_user_message.lower():
            return f"Good answer about version control. Now let's talk about problem-solving. Can you describe a time when you had to debug a difficult issue? What was your approach?\n\n*(Response generated at {timestamp})*"

        elif 'debug' in last_user_message or 'problem' in last_user_message:
            return f"Excellent debugging approach. Let's discuss system design. How would you design a scalable web application that needs to handle millions of users?\n\n*(Response generated at {timestamp})*"

        elif 'design' in last_user_message or 'scalable' in last_user_message:
            return f"Great insights on system design. One more question: How do you stay updated with the latest technologies and best practices in your field?\n\n*(Response generated at {timestamp})*"

        elif 'stay updated' in last_user_message or 'latest' in last_user_message:
            return f"Thank you for your thoughtful responses throughout this interview. I appreciate you taking the time to share your experiences and technical knowledge with me. The interview is now complete. Your responses will be reviewed by our team.\n\n*(Response generated at {timestamp})*"

        else:
            return f"Thank you for your response. That's very interesting. Can you elaborate a bit more on that topic or give me a specific example from your experience?\n\n*(Response generated at {timestamp})*"

    async def _send_real_api_request(self, conversation_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send actual API request to the external AI service.
        This method is ready for when we want to enable real API calls.
        """
        if not HTTPX_AVAILABLE:
            return {
                "status": "failed",
                "success": False,
                "error": "httpx library not available",
                "text": "I apologize, but I'm experiencing technical difficulties. Please try again."
            }

        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=conversation_payload
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"AI API error: {response.status_code} - {response.text}")
                    return {
                        "status": "failed",
                        "success": False,
                        "error": f"API returned {response.status_code}",
                        "text": "I apologize, but I'm experiencing technical difficulties. Please try again."
                    }

        except Exception as e:
            logger.error(f"AI API request failed: {str(e)}")
            return {
                "status": "failed",
                "success": False,
                "error": str(e),
                "text": "I apologize, but I'm experiencing technical difficulties. Please try again."
            }

    def validate_ai_response(self, response: Dict[str, Any]) -> bool:
        """Validate the structure of AI response."""
        required_fields = ['status', 'success', 'text', 'requestId']
        return all(field in response for field in required_fields)

    def extract_response_text(self, response: Dict[str, Any]) -> Optional[str]:
        """Extract the text content from AI response."""
        if response.get('success') and response.get('status') == 'succeeded':
            return response.get('text')
        return None
