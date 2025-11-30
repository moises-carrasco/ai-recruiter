"""
Interview link generation utilities.
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional


def generate_unique_interview_link(interview_id: int) -> str:
    """
    Generate a unique, cryptographically secure interview link.

    Combines interview ID with a random token for security.
    """
    # Generate a secure random token
    token = secrets.token_urlsafe(32)  # 32 bytes = 43 characters

    # Create a hash of interview_id + token for additional security
    hash_input = f"{interview_id}:{token}"
    link_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    # Create the link: interview/{hash}
    return f"interview/{link_hash}"


def validate_link_expiration(
    scheduled_datetime: str,
    current_datetime: Optional[str] = None,
    tolerance_minutes: int = 5
) -> bool:
    """
    Validate if the current time is within the allowed window for interview access.

    Args:
        scheduled_datetime: ISO8601 scheduled time
        current_datetime: ISO8601 current time (defaults to now)
        tolerance_minutes: Minutes before/after scheduled time to allow access

    Returns:
        True if access is allowed, False otherwise
    """
    try:
        scheduled = datetime.fromisoformat(scheduled_datetime.replace('Z', '+00:00'))

        if current_datetime:
            current = datetime.fromisoformat(current_datetime.replace('Z', '+00:00'))
        else:
            current = datetime.utcnow()

        # Calculate time window
        window_start = scheduled - timedelta(minutes=tolerance_minutes)
        window_end = scheduled + timedelta(minutes=tolerance_minutes)

        return window_start <= current <= window_end

    except (ValueError, AttributeError):
        return False


def create_secure_token(length: int = 32) -> str:
    """
    Create a cryptographically secure random token.

    Args:
        length: Length of the token in bytes

    Returns:
        URL-safe base64 encoded token
    """
    return secrets.token_urlsafe(length)


def verify_link_token(token: str, expected_hash: str) -> bool:
    """
    Verify that a token matches an expected hash.

    Args:
        token: The token to verify
        expected_hash: The expected SHA256 hash

    Returns:
        True if token is valid, False otherwise
    """
    computed_hash = hashlib.sha256(token.encode()).hexdigest()
    return secrets.compare_digest(computed_hash, expected_hash)


def generate_link_expiration_datetime(scheduled_datetime: str, tolerance_minutes: int = 5) -> str:
    """
    Generate the expiration datetime for an interview link.

    Args:
        scheduled_datetime: ISO8601 scheduled time
        tolerance_minutes: Minutes to add to scheduled time

    Returns:
        ISO8601 expiration datetime
    """
    scheduled = datetime.fromisoformat(scheduled_datetime.replace('Z', '+00:00'))
    expires_at = scheduled + timedelta(minutes=tolerance_minutes)
    return expires_at.isoformat()
