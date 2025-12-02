"""
Dashboard service for statistics and metrics operations.
"""

from typing import Dict, Any
from sqlalchemy.orm import Session
from ..repositories.interview_repo import InterviewRepository
from ..repositories.candidate_repo import CandidateRepository
from ..core.logging_config import get_logger


class DashboardService:
    """Service for dashboard statistics and metrics."""

    def __init__(self):
        self.interview_repo = InterviewRepository()
        self.candidate_repo = CandidateRepository()
        self.logger = get_logger(__name__)

    async def get_dashboard_statistics(self, db: Session) -> Dict[str, Any]:
        """
        Get all dashboard statistics.

        Returns:
            Dict containing:
            - total_interviews: Total number of interviews
            - completed_interviews: Number of completed interviews
            - pending_interviews: Always 0 as specified
            - active_candidates: Number of active candidates
        """
        try:
            # Get statistics from repositories
            total_interviews = await self.interview_repo.count_total_interviews(db)
            completed_interviews = await self.interview_repo.count_completed_interviews(db)
            active_candidates = await self.candidate_repo.count_active_candidates(db)

            # Pending interviews is set to 0 as per user requirement
            pending_interviews = 0

            statistics = {
                "total_interviews": total_interviews,
                "completed_interviews": completed_interviews,
                "pending_interviews": pending_interviews,
                "active_candidates": active_candidates
            }

            self.logger.info(f"Dashboard statistics retrieved: {statistics}")
            return statistics

        except Exception as e:
            self.logger.error(f"Error retrieving dashboard statistics: {str(e)}")
            # Return zeros in case of error to prevent UI crashes
            return {
                "total_interviews": 0,
                "completed_interviews": 0,
                "pending_interviews": 0,
                "active_candidates": 0
            }
