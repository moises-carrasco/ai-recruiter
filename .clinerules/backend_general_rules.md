# Backend General Rules (FastAPI + SQLAlchemy + Pydantic)

These rules define the global backend conventions for this project.  
Cline MUST follow these rules when generating or modifying backend code.

## 1. Project Architecture Principles
- The backend strictly follows this structure:
  - Routers (API layer)
  - Services (business logic)
  - Repositories (DB access)
  - SQLAlchemy models
  - Pydantic schemas
  - DB session initialization
- No business logic is allowed inside routers.
- The service layer must be the only layer calling repositories.
- Repositories must not import from services.
- Circular imports must be avoided.

## 2. Code Style and Naming Conventions
- snake_case for functions, vars, modules.
- PascalCase for models and schemas.
- UPPERCASE for constants.
- Filenames must be descriptive: `interview_service.py`, `user_repo.py`, etc.
- Avoid abbreviations unless they are industry-standard (ID, API, JWT).

## 3. Response & Error Handling Rules
- Use Pydantic schemas at all times.
- Never return raw SQLAlchemy models.
- Use HTTPException for errors.
- When raising HTTP errors, use:
```python
from fastapi import HTTPException, status
raise HTTPException(status_code=..., detail="...")
- Validation happens in service layer, not at the repository layer.

## 4. Logging Rules
- Use logging_config.py only.
- Services must log:
  - Start and end of important operations
  - AI interactions
  - Failed operations
  - Security-sensitive events (login attempts, permission issues)

## 5. Authentication & Security Rules
- Use JWT auth.
- Hash passwords via core/security.py.
- No sensitive data in responses.

## 6. Environment Configuration Rules
- Load everything from config.py.
- No hardcoded secrets or connection strings.
- Always rely on Settings() dependency injection.

## 7. AI Integration Rules
- AI logic only inside ai_agent_service.py.
- Prompts must follow ai_prompts.md.
- All LLM interactions must go through ai_agent_service.py.
- Validate AI outputs.

## 8. File Organization Rules
- Follow existing folder structure.
- Shared utilities go in app/utils/.

## 9. SOLID Principles Implementation
- **Single Responsibility Principle (SRP):**
  - Each service class must handle only one business domain
  - Repositories must only handle data access for one entity
  - Routers must only handle HTTP concerns for one resource
- **Open/Closed Principle (OCP):**
  - Extend functionality through new services/repositories, not modification
  - Use dependency injection to allow behavior extension
  - AI agent service must be extensible for new interview types
- **Liskov Substitution Principle (LSP):**
  - Repository implementations must be interchangeable
  - Service interfaces must be consistent across implementations
- **Interface Segregation Principle (ISP):**
  - Create specific repository interfaces for different data access needs
  - Avoid fat service interfaces that force unnecessary dependencies
- **Dependency Inversion Principle (DIP):**
  - Services must depend on repository abstractions, not concrete implementations
  - High-level modules (services) must not depend on low-level modules (repositories)
  - Use dependency injection for all cross-layer dependencies

## 10. Design Pattern Guidelines
- **Repository Pattern (Required):**
  - Encapsulate data access logic in repository classes
  - Provide consistent interface for data operations
  - Enable easy testing through repository mocking
- **Strategy Pattern (Recommended for):**
  - Different AI interview approaches based on role/seniority
  - Multiple authentication methods
  - Various feedback generation algorithms
- **Factory Pattern (Use for):**
  - Creating complex domain entities with validation
  - Generating different types of interview configurations
  - Building AI prompts based on context
- **Observer Pattern (Consider for):**
  - Interview status change notifications
  - Audit logging across services
  - Real-time updates during interview execution
- **Adapter Pattern (Use for):**
  - External AI service integration
  - File upload/processing services
  - Third-party authentication providers

## 11. Testing Rules
- Light tests: routers (smoke), services logic, AI stubs.
