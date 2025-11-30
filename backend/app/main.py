"""
FastAPI main application entry point.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))  # Agrega el root del proyecto al path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import settings

app = FastAPI(
    title="AI Technical Interview System",
    description="MVP web application for AI-conducted technical interviews",
    version="1.0.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"message": "AI Technical Interview System API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
