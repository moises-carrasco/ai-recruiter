#!/usr/bin/env python3
"""
Test script for AI Agent Service
"""

import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.ai_agent_service import AIAgentService


async def test_ai_service(mock_mode: bool = True):
    """Test the AI agent service with a sample conversation payload."""
    print(f"\n{'='*50}")
    print(f"Testing AI Agent Service (mock_mode={mock_mode})")
    print(f"{'='*50}")

    service = AIAgentService(mock_mode=mock_mode)

    # Sample conversation payload as per chatLogic.md
    test_payload = {
        "assistant": "Interviewer_Expert",
        "messages": [
            {
                "role": "user",
                "content": "Hello, I am ready for the technical interview. I have 5 years of experience in software development."
            }
        ],
        "revision": 3,
        "revisionName": "3"
    }

    print("Sending test message to AI assistant...")
    print(f"Payload: {test_payload}")

    try:
        response = await service.send_chat_message(test_payload)

        print("\n=== AI Response ===")
        print(f"Status: {response.get('status')}")
        print(f"Success: {response.get('success')}")
        print(f"Request ID: {response.get('requestId')}")

        if response.get('success') and response.get('status') == 'succeeded':
            print(f"AI Text Response: {response.get('text')}")
            print("\n✅ Test PASSED: AI responded successfully!")
        else:
            print(f"Error: {response.get('error', 'Unknown error')}")
            print("\n❌ Test FAILED: AI did not respond successfully")

        # Additional validation
        if service.validate_ai_response(response):
            print("✅ Response validation: PASSED")
        else:
            print("❌ Response validation: FAILED")

        return True

    except Exception as e:
        print(f"\n❌ Test FAILED with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run tests for both mock and real modes."""
    print("Starting AI Agent Service Tests")

    # Test mock mode
    mock_test_passed = await test_ai_service(mock_mode=True)

    # Test real mode (if httpx is available)
    try:
        import httpx
        print("\nNote: httpx is available, testing real mode...")
        real_test_passed = await test_ai_service(mock_mode=False)
    except ImportError:
        print("\nNote: httpx not available, skipping real mode test")
        real_test_passed = None

    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Mock Mode Test: {'PASSED' if mock_test_passed else 'FAILED'}")
    if real_test_passed is not None:
        print(f"Real Mode Test: {'PASSED' if real_test_passed else 'FAILED'}")
    else:
        print("Real Mode Test: SKIPPED (httpx not available)")

    if mock_test_passed and (real_test_passed is None or real_test_passed):
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")


if __name__ == "__main__":
    asyncio.run(main())
