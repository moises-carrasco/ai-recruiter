# Technical Context

## Technology Stack Overview

### Backend Technology Stack
- **Framework:** FastAPI (Python)
- **ORM:** SQLAlchemy
- **Data Validation:** Pydantic
- **Database:** SQLite
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** bcrypt via passlib
- **File Handling:** Python standard library
- **AI Integration:** External AI service (OpenAI API or similar)

### Frontend Technology Stack
- **Framework:** Vue 3 with Composition API
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **State Management:** Pinia (Vue 3 store)
- **Routing:** Vue Router 4
- **UI Components:** Custom components with Tailwind

### Development Tools
- **Package Management:** 
  - Backend: pip with requirements.txt
  - Frontend: npm with package.json
- **Code Quality:** ESLint (frontend), Black/Flake8 (backend)
- **Version Control:** Git
- **Environment Management:** Python virtual environments, Node.js

## Architecture Patterns

### Backend Architecture
```
API Layer (FastAPI Routers)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Data Access)
    ↓
Database Layer (SQLite + SQLAlchemy)
```

### Frontend Architecture
```
Views (Page Components)
    ↓
Components (Reusable UI)
    ↓
Store (Pinia State Management)
    ↓
Services/API (HTTP Communication)
```

## Project Structure

### Backend Structure
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── candidates.py
│   │       │   ├── interviews.py
│   │       │   └── lookup.py
│   │       └── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging_config.py
│   ├── models/
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── candidate.py
│   │   ├── interview.py
│   │   └── lookup.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── candidate.py
│   │   ├── interview.py
│   │   └── lookup.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── candidate_service.py
│   │   ├── interview_service.py
│   │   ├── lookup_service.py
│   │   └── ai_agent_service.py
│   ├── repositories/
│   │   ├── base.py
│   │   ├── user_repo.py
│   │   ├── candidate_repo.py
│   │   ├── interview_repo.py
│   │   └── lookup_repo.py
│   ├── db/
│   │   ├── session.py
│   │   └── init_db.py
│   ├── utils/
│   │   ├── file_handler.py
│   │   └── link_generator.py
│   └── main.py
├── tests/
├── requirements.txt
└── README.md
```

### Frontend Structure
```
frontend/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── common/
│   │   │   ├── NavigationBar.vue
│   │   │   ├── LoadingSpinner.vue
│   │   │   └── ErrorMessage.vue
│   │   ├── forms/
│   │   │   ├── CandidateForm.vue
│   │   │   ├── InterviewForm.vue
│   │   │   └── UserForm.vue
│   │   └── lists/
│   │       ├── CandidateList.vue
│   │       ├── InterviewList.vue
│   │       └── FilterControls.vue
│   ├── views/
│   │   ├── HomeView.vue
│   │   ├── CandidatesView.vue
│   │   ├── InterviewsView.vue
│   │   ├── InterviewDetailView.vue
│   │   ├── LoginView.vue
│   │   └── InterviewExecutionView.vue
│   ├── router/
│   │   └── index.js
│   ├── store/
│   │   ├── auth.js
│   │   ├── candidates.js
│   │   ├── interviews.js
│   │   └── lookup.js
│   ├── utils/
│   │   ├── api.js
│   │   ├── auth.js
│   │   └── validators.js
│   ├── composables/
│   │   ├── useAuth.js
│   │   ├── useApi.js
│   │   └── useFilters.js
│   ├── App.vue
│   └── main.js
├── public/
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Development Setup

### Backend Setup

1. **Environment Variables:**
   ```bash
   # .env file
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///./interview_system.db
   AI_API_KEY=your-ai-service-api-key
   AI_API_URL=https://api.openai.com/v1
   ```

2. **Database Initialization:**
   ```bash
   python -m app.db.init_db
   ```

3. **Run Development Server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Environment Variables:**
   ```bash
   # .env file
   VITE_API_BASE_URL=http://localhost:8000/api/v1
   ```

3. **Run Development Server:**
   ```bash
   npm run dev
   ```

## Configuration Management

### Backend Configuration
- **config.py:** Centralized configuration using Pydantic Settings
- **Environment Variables:** All sensitive data via environment variables
- **Database Configuration:** SQLite connection string and settings
- **AI Service Configuration:** API keys and endpoints
- **Security Configuration:** JWT settings, password hashing parameters

### Frontend Configuration
- **vite.config.js:** Build and development server configuration
- **tailwind.config.js:** Tailwind CSS customization
- **Environment Variables:** API endpoints and feature flags

## Database Configuration

### SQLite Setup
- **File Location:** `./interview_system.db` (relative to backend root)
- **Connection Pooling:** SQLAlchemy connection pool
- **Foreign Keys:** Enabled via PRAGMA foreign_keys = ON
- **WAL Mode:** Enabled for better concurrent access

### Migration Strategy
- **Alembic:** Database migration tool (if needed for production)
- **Init Scripts:** Database initialization scripts in `db/init_db.py`
- **Seed Data:** Initial lookup table data population

## API Design

### RESTful Endpoints
- **Base URL:** `/api/v1`
- **Authentication:** Bearer token in Authorization header
- **Content Type:** JSON for request/response bodies
- **Status Codes:** Standard HTTP status codes
- **Error Format:** Consistent error response structure

### API Versioning
- **URL Versioning:** `/api/v1/` prefix for all endpoints
- **Backward Compatibility:** Maintain v1 compatibility for MVP
- **Future Versions:** `/api/v2/` for breaking changes

## Security Configuration

### Authentication & Authorization
- **JWT Tokens:** Access tokens with configurable expiration
- **Password Hashing:** bcrypt with salt rounds
- **Role-Based Access:** User roles enforced at service layer
- **CORS:** Configured for frontend domain

### Data Security
- **Input Validation:** Pydantic schemas for all inputs
- **SQL Injection Prevention:** SQLAlchemy ORM parameterized queries
- **File Upload Security:** File type validation and secure storage
- **Sensitive Data:** No sensitive data in logs or error messages

## AI Integration

### External AI Service
- **Provider:** OpenAI API (configurable for other providers)
- **Authentication:** API key-based authentication
- **Rate Limiting:** Respect provider rate limits
- **Error Handling:** Graceful degradation on AI service failures

### AI Service Configuration
- **Model Selection:** Configurable AI model (e.g., GPT-3.5, GPT-4)
- **Prompt Templates:** Structured prompts for consistent responses
- **Response Parsing:** Structured response validation
- **Timeout Handling:** Configurable timeout for AI requests

## Performance Considerations

### Backend Performance
- **Database Indexing:** Strategic indexes on frequently queried columns
- **Connection Pooling:** SQLAlchemy connection pool management
- **Async Operations:** FastAPI async/await for I/O operations
- **Caching:** In-memory caching for lookup data

### Frontend Performance
- **Code Splitting:** Vite automatic code splitting
- **Lazy Loading:** Route-based lazy loading
- **Asset Optimization:** Vite build optimization
- **API Caching:** Intelligent API response caching

## Development Constraints

### Technical Constraints
- **SQLite Limitations:** Single-writer limitation for concurrent access
- **File Storage:** Local file system storage (no cloud storage)
- **AI Dependencies:** External AI service dependency
- **Browser Support:** Modern browsers only (ES6+ support)

### Development Environment
- **Python Version:** Python 3.8+
- **Node.js Version:** Node.js 16+
- **Operating System:** Cross-platform (Windows, macOS, Linux)
- **IDE Support:** VS Code recommended with extensions

## Testing Strategy

### Backend Testing
- **Unit Tests:** pytest for service and repository layers
- **Integration Tests:** FastAPI TestClient for API endpoints
- **Database Tests:** In-memory SQLite for test isolation
- **AI Service Mocking:** Mock AI responses for consistent testing

### Frontend Testing
- **Unit Tests:** Vitest for component testing
- **Integration Tests:** Vue Test Utils for component integration
- **E2E Tests:** Playwright for end-to-end scenarios
- **API Mocking:** Mock API responses for frontend testing

## Deployment Considerations

### Production Requirements
- **Database:** Consider PostgreSQL for production scalability
- **File Storage:** Cloud storage for file uploads
- **Environment Variables:** Secure environment variable management
- **Logging:** Structured logging with log aggregation
- **Monitoring:** Application performance monitoring
- **Backup Strategy:** Database and file backup procedures

### Scalability Considerations
- **Database Migration:** Plan for SQLite to PostgreSQL migration
- **Load Balancing:** Multiple backend instances behind load balancer
- **CDN:** Static asset delivery via CDN
- **Caching Layer:** Redis for session and data caching
