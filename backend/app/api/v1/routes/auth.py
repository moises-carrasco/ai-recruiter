"""
Authentication routes for login and token management.
"""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement authentication endpoints
# - POST /login
# - POST /logout
# - GET /me (current user info)

@router.get("/health")
async def auth_health():
    """Health check for auth module."""
    return {"status": "ok", "module": "auth"}
