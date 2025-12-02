"""
Dashboard routes for statistics and metrics.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter()


def get_dashboard_service() -> DashboardService:
    """Dependency to get dashboard service."""
    return DashboardService()


@router.get("/statistics", status_code=status.HTTP_200_OK)
async def get_dashboard_statistics(
    db: Session = Depends(get_db),
    service: DashboardService = Depends(get_dashboard_service)
):
    """
    Get dashboard statistics.

    Returns statistics including:
    - total_interviews: Total number of interviews
    - completed_interviews: Number of completed interviews
    - pending_interviews: Number of pending interviews (set to 0)
    - active_candidates: Number of active candidates
    """
    try:
        statistics = await service.get_dashboard_statistics(db)
        return statistics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving dashboard statistics: {str(e)}"
        )
