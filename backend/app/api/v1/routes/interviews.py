"""
Interview management and execution routes.
"""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement interview endpoints
# - GET /interviews (list interviews with filters)
# - POST /interviews (create interview)
# - GET /interviews/{interview_id} (get interview by id)
# - PUT /interviews/{interview_id} (update interview)
# - DELETE /interviews/{interview_id} (delete interview)
# - GET /interviews/link/{interview_link} (access interview by link)
# - POST /interviews/{interview_id}/start (start interview)
# - POST /interviews/{interview_id}/complete (complete interview)
# - GET /interviews/{interview_id}/feedback (get interview feedback)

@router.get("/health")
async def interviews_health():
    """Health check for interviews module."""
    return {"status": "ok", "module": "interviews"}
