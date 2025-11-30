"""
User management routes.
"""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement user endpoints
# - GET /users (list users)
# - POST /users (create user)
# - GET /users/{user_id} (get user by id)
# - PUT /users/{user_id} (update user)
# - DELETE /users/{user_id} (delete user)

@router.get("/health")
async def users_health():
    """Health check for users module."""
    return {"status": "ok", "module": "users"}
