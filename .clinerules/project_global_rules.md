# Global Project Rules
These rules define the overarching guidelines and constraints for the entire project.  
They apply to both backend and frontend, as well as AI/LLM integration.  
Cline MUST follow these rules when generating or modifying any part of the system.

---

# ================================================
# 1. Foundational Principles of the Project
# ================================================

## 1.1 Architecture Philosophy
- The project follows a **clean layered architecture**:
  - Backend: Routers → Services → Repositories → DB
  - Frontend: Views → Components → Store → Services/API
- Business logic must only exist in:
  - services (backend)
  - store or composables (frontend)

## 1.2 Separation of Concerns
- Backend handles: logic, data, domain rules, AI integration.
- Frontend handles: UI, user interaction, minimal state transitions.
- No backend logic on frontend, and no UI logic on backend.
- AI agent logic is isolated in a dedicated backend service file.

## 1.3 Project Goal Alignment
- All generated code MUST align with:
  - `requirements.md`
  - `userstories.md`
  - `datamodel.md`
  - `ai_prompts.md`
- If a conflict arises, **requirements.md takes priority**.

---

# ================================================
# 2. Naming, Structure & Consistency Rules
# ================================================

## 2.1 Naming Conventions
- The same entities MUST share names across:
  - models
  - schemas
  - routers
  - services
  - repositories
  - frontend store
  - API responses
- Avoid synonyms (e.g., “candidate” vs “applicant”). Pick one and keep it everywhere.

## 2.2 File & Folder Organization
- No new top-level folders without architectural justification.
- Backend & frontend must follow their predefined folder structure.
- New features must be added consistently:
  - one backend router + one service + one repo + schemas + model
  - one frontend view + store update + services/api calls

## 2.3 API Versioning
- All endpoints MUST be placed inside `api/v1/`.
- New versions (if needed) will follow `v2`, but not mix concepts.

---

# ================================================
# 3. Data, Types & Validation Rules
# ================================================

## 3.1 Source of Truth for Data Model
- `datamodel.md` is the canonical reference for:
  - entity structures
  - relationships
  - field names
  - IDs
  - data constraints

## 3.2 Validation Responsibilities
- Backend performs:
  - domain validation
  - data integrity checks
  - business rule enforcement
- Frontend performs:
  - UI-level validation
  - friendly error messaging

## 3.3 Type Consistency
- Data types must match across backend → API → frontend.
- IDs must consistently be `int` unless specified otherwise.
- Timestamps must be ISO 8601.

---

# ================================================
# 4. API & Communication Rules
# ================================================

## 4.1 API Design
- Backend must expose clean RESTful endpoints.
- Endpoints must:
  - return Pydantic schemas
  - use explicit status codes
  - follow nouns, not verbs (`/interviews`, not `/getInterview`)

## 4.2 Error Handling
- Errors must follow consistent structure:
  `{ "detail": "Human-readable message" }`
- Frontend must always display meaningful errors to the user.

## 4.3 Cross-Layer Boundaries
- Frontend must NEVER bypass API or mock domain rules.
- Backend must NEVER depend on frontend structures.

---

# ================================================
# 5. AI / LLM Integration Rules
# ================================================

## 5.1 Single Access Point
- The backend’s `ai_agent_service.py` is the ONLY entrypoint to the AI.
- No other backend layer or frontend module may call an LLM directly.

## 5.2 Prompt & Role Governance
- Prompts MUST be defined or referenced from `ai_prompts.md`.
- No hardcoded prompts in code unless small helper templates.
- Prompt formatting must be standardized.

## 5.3 AI Safety & Output Handling
- AI outputs must be validated before persistence or sending to frontend.
- The system must gracefully handle:
  - empty responses
  - malformed responses
  - hallucinations
  - long delays

## 5.4 Deterministic Behavior for Scoring
- AI scoring or analysis must use consistent templates.
- Avoid randomness unless explicitly required.

---

# ================================================
# 6. Code Quality & Maintainability Rules
# ================================================

## 6.1 Style Consistency
- Backend uses PEP8.
- Frontend uses project-wide Vue style & Tailwind conventions.

## 6.2 Documentation & Comments
- Functions must include meaningful docstrings or comments when needed.
- Complex flows (AI workflows, interview scoring) MUST be documented.

## 6.3 Avoiding Duplication
- Shared utilities must be kept in:
  - `app/utils/` (backend)
  - `src/utils/` or `src/composables/` (frontend)
- No repeated API logic.

## 6.4 SOLID Principles Enforcement
- All layers must adhere to SOLID principles as defined in their respective rule files
- Cross-layer interactions must respect dependency inversion principle
- Single responsibility must be maintained across all modules and components
- Extension over modification must be preferred for new functionality

## 6.5 Design Pattern Selection Guidelines
- **Backend Patterns:**
  - Repository pattern is mandatory for data access
  - Strategy pattern for AI interview variations and business logic alternatives
  - Factory pattern for complex entity creation and configuration
  - Adapter pattern for external service integrations
- **Frontend Patterns:**
  - Composition pattern is required for component architecture
  - Observer pattern through Vue's reactivity for state management
  - Factory pattern for dynamic UI generation
  - Strategy pattern for conditional rendering and validation
- **Cross-Layer Patterns:**
  - Adapter pattern for API integration and data transformation
  - Observer pattern for real-time updates and notifications
  - Command pattern for complex user actions that span multiple layers

---

# ================================================
# 7. Testing & Stability Rules
# ================================================

## 7.1 PoC Testing Scope
- Backend:
  - routers → smoke tests
  - services → core logic tests
  - AI agent → prompt formatting tests
- Frontend:
  - smoke tests for views
  - isolated component tests for critical UI parts
- No need for full coverage, but critical paths must be validated.

---

# ================================================
# 8. Deployment, Config & Environment
# ================================================

## 8.1 Environment Handling
- All backend config must come from environment variables or config.py.
- No secrets in code.
- Frontend API URL must be set via env variables.

## 8.2 Build Consistency
- Vite build must always succeed without warnings.
- Backend must start without raising import or dependency errors.

---

# ================================================
# 9. Project Evolution Rules
# ================================================

## 9.1 If the project grows
- Split backend & frontend rules into more files as needed.
- Introduce modular architecture when complexity increases.
- Add API versioning as features evolve.

## 9.2 Cline Integration
- Cline MUST always check:
  - system_requirements.md
  - userstories.md
  - datamodel.md
  - ai_prompts.md
  before generating new functionality.

---

# ================================================
# 10. Language & Output Rules
# ================================================
- All code, comments, documentation, variable names, function names, filenames, commit messages, API responses, and any generated content MUST be written strictly in **English**.
- Cline MUST NOT generate content in Spanish or any other language unless explicitly instructed for a specific case.
- Error messages, logs, console output, and user-facing UI text MUST also be in English.
- Technical explanations, architectural notes, and reasoning provided by Cline MUST be in English.
- If the user asks something in Spanish, Cline MUST still generate code and documentation in English unless the user explicitly says otherwise

---

# End of Global Project Rules
