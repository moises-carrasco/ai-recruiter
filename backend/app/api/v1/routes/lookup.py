"""
Lookup table management routes.
"""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement lookup endpoints
# - GET /lookup (get all lookup items)
# - GET /lookup/{domain} (get items by domain)
# - POST /lookup (create lookup item)
# - PUT /lookup/{lookup_id} (update lookup item)
# - DELETE /lookup/{lookup_id} (delete lookup item)
# - GET /lookup/roles (get all roles)
# - GET /lookup/clients (get all clients)
# - GET /lookup/seniorities (get all seniorities)
# - GET /lookup/statuses (get all interview statuses)

@router.get("/health")
async def lookup_health():
    """Health check for lookup module."""
    return {"status": "ok", "module": "lookup"}
