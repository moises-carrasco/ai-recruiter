"""
API v1 router initialization.
"""

from fastapi import APIRouter

from app.api.v1.routes import auth, users, candidates, interviews, lookup, dashboard

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(candidates.router, prefix="/candidates", tags=["candidates"])
api_router.include_router(interviews.router, prefix="/interviews", tags=["interviews"])
api_router.include_router(lookup.router, prefix="/lookup", tags=["lookup"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
