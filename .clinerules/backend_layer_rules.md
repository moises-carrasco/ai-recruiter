# Backend Layer-Specific Rules

Rules for each backend layer.

# ==========================
# 1. Rules for Routers (API)
# ==========================

- Only handle HTTP semantics.
- No business logic.
- Must call services.
- Must return Pydantic schemas.
- Must declare endpoints and methods.
- Must be async.
- Translate service outputs into API responses.
- Must not query the database directly.
- Must not call repositories.
- Validate input via Pydantic schemas
- Router files must be located at `app/api/v1/routes/*.py`
- All routes must be included in `api/v1/__init__.py`
- Endpoints must return Pydantic schema or list thereof.
- Endpoints must specify status codes explicitly.
- Endpoints must use dependency injection for user authentication if needed.
- Example router pattern:

```python
@router.get("/", response_model=List[InterviewOut])
async def get_interviews(service: InterviewService = Depends()):
    return await service.get_interviews()



# 2. Services Layer
- Contains business logic.
- Validates/sanitize data.
- Orchestrate multiple repositories
- Service must prepare AI prompts and call AI agent service
- Calls AI agent service.
- Does NOT execute SQL.
- Raise business errors as HTTP exceptions when needed.
- Services must NOT execute SQLAlchemy queries directly.
- Services must NOT contain FastAPI imports (except HTTPException).
- Services must NOT depend on request or response objects.
- Services are located at app/services/*.py
- Service methods should be async.


# 3. Repositories Layer
- Direct SQLAlchemy access.
- No HTTPException.
- No Pydantic schemas.
- No business logic.
- They must receive a DB session
- They must perform CRUD operations
- They must return SQLAlchemy model instances
- They must not raise HTTPExceptions (raise generic exceptions instead)
- They must not return Pydantic schemas
- They must not perform input validation
- Repositories are located at app/repositories/*.py
- Standard repository method structure: 
async def get_by_id(self, db: Session, id: int):
    return db.query(Model).filter(Model.id == id).first()

# 4. Models & Schemas
## SQLAlchemy Models
- Located in: app/models/
- Must inherit from Base in models/base.py
- Use explicit column definitions
- Relationships must be declared consistently
- Avoid circular relationships

## Pydantic Schemas
- Use orm_mode.
- Separate create/update/out schemas.
- Located in: app/schemas/
- Must be grouped by domain (user.py, interview.py)


# 5. DB Access
- DB session from app/db/session.py.
- No manual session creation.
- Services that need DB sessions must receive them via dependency injection.
- DB initialization must occur only in init_db.py.
- Never create sessions manually inside routers or random functions.

# 6. Layer Interaction Rules
- Routers → Services → Repositories → DB
- No layer may skip the one below it.
- AI agent integration is ONLY allowed at the service layer.