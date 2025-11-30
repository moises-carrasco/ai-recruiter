# Active Context

## Current Work Focus

### Primary Objective
Initialize the memory bank for the AI Technical Interview System project with comprehensive documentation covering all aspects of the system architecture, requirements, and implementation guidelines.

### Recent Activities
- **Memory Bank Initialization:** Created foundational documentation structure following .clinerules memory bank guidelines
- **Requirements Analysis:** Documented functional and non-functional requirements based on project definition
- **Data Model Design:** Defined complete database schema with relationships and constraints
- **Architecture Documentation:** Established technical stack and system patterns

### Current Implementation Status
**Phase:** Project Planning and Documentation
**Status:** Memory Bank Initialization Complete
**Next Phase:** Backend Foundation Setup

## Active Decisions and Considerations

### Architecture Decisions
1. **Layered Architecture:** Strict separation between routers, services, repositories, and models
2. **Repository Pattern:** Mandatory for all data access operations
3. **Dependency Injection:** FastAPI dependency system for service management
4. **Generic Lookup Table:** Single table for all reference data (roles, clients, seniorities)

### Technology Stack Decisions
1. **Backend:** FastAPI + SQLAlchemy + Pydantic for robust API development
2. **Frontend:** Vue 3 Composition API + Tailwind for modern, reactive UI
3. **Database:** SQLite for MVP simplicity with PostgreSQL migration path
4. **AI Integration:** External AI service (OpenAI API) with adapter pattern

### Data Model Decisions
1. **Snake_case Convention:** All database tables and columns use snake_case
2. **Audit Columns:** created_at and updated_at mandatory for all tables
3. **Soft Delete:** is_active column for users, candidates, and lookup items
4. **Foreign Key Constraints:** Strict referential integrity with cascade deletes for dependent data

### Security Decisions
1. **JWT Authentication:** Token-based authentication with role-based access control
2. **Password Hashing:** bcrypt for secure password storage
3. **Input Validation:** Pydantic schemas for all API inputs
4. **File Upload Security:** Type validation and secure storage paths

## Important Patterns and Preferences

### Backend Patterns
- **Service Layer:** All business logic encapsulated in service classes
- **Error Handling:** Centralized error handling with consistent HTTP exceptions
- **AI Integration:** Single point of access through ai_agent_service.py
- **Validation:** Business rules validated at service layer, not repository layer

### Frontend Patterns
- **Composition API:** Vue 3 composables for reusable logic
- **State Management:** Pinia stores for centralized state
- **Component Communication:** Props down, events up pattern
- **Error Handling:** Centralized error handling with user-friendly messages

### Code Quality Standards
- **Naming Conventions:** PascalCase for classes, snake_case for functions/variables
- **Documentation:** Comprehensive docstrings for complex business logic
- **Testing:** Repository mocking for service layer tests
- **Logging:** Structured logging for AI interactions and business operations

## Learnings and Project Insights

### Key Technical Insights
1. **Generic Lookup Table:** Provides flexibility for managing reference data without schema changes
2. **Interview Link Security:** Cryptographically secure links with time-based validation
3. **AI Service Isolation:** Dedicated service layer prevents AI logic from spreading across the application
4. **File Upload Strategy:** Local storage for MVP with cloud migration path

### Business Logic Insights
1. **Interview Workflow:** Clear state transitions from registered → executed → completed
2. **Feedback Structure:** JSON-based skills evaluation allows flexible skill assessment
3. **Role-Based Access:** Three distinct user roles with specific permissions
4. **Time-Sensitive Links:** ±5 minute tolerance balances security with usability

### Integration Considerations
1. **AI Service Reliability:** Circuit breaker pattern for handling AI service failures
2. **Database Scalability:** SQLite limitations require PostgreSQL migration planning
3. **File Storage:** Local file system adequate for MVP, cloud storage for production
4. **Frontend-Backend Communication:** RESTful API with consistent error responses

## Current Challenges and Solutions

### Technical Challenges
1. **SQLite Concurrency:** Single-writer limitation addressed through connection pooling
2. **AI Service Dependency:** External service reliability managed through fallback mechanisms
3. **File Upload Size:** 10MB limit balances functionality with performance
4. **Interview Link Security:** Unique, time-sensitive links prevent unauthorized access

### Business Challenges
1. **Objective Assessment:** AI limited to quantifiable technical attributes only
2. **Interview Standardization:** Consistent evaluation criteria across different roles
3. **User Experience:** Balance between comprehensive data collection and ease of use
4. **Scalability Planning:** MVP architecture supports future enterprise features

## Next Steps and Priorities

### Immediate Next Steps
1. **Backend Foundation:** Set up FastAPI project structure with core configuration
2. **Database Setup:** Create SQLite database with initial schema and seed data
3. **Authentication System:** Implement JWT-based authentication and user management
4. **Core Models:** Create SQLAlchemy models for all entities

### Short-term Priorities
1. **Repository Layer:** Implement base repository and entity-specific repositories
2. **Service Layer:** Create service classes with business logic and validation
3. **API Endpoints:** Develop RESTful endpoints for CRUD operations
4. **Frontend Foundation:** Set up Vue 3 project with Tailwind and routing

### Medium-term Goals
1. **AI Integration:** Implement AI agent service with prompt management
2. **Interview Workflow:** Complete interview scheduling and execution flow
3. **File Upload System:** Implement secure file upload and storage
4. **Feedback Generation:** Create structured feedback system with rankings

### Long-term Considerations
1. **Production Deployment:** Plan for PostgreSQL migration and cloud deployment
2. **Performance Optimization:** Implement caching and query optimization
3. **Monitoring and Logging:** Add comprehensive application monitoring
4. **Feature Extensions:** Plan for advanced reporting and analytics

## Project Context Reminders

### Core Constraints
- **Assessment Scope:** Technical competencies only, no behavioral evaluation
- **MVP Focus:** Essential features only, advanced capabilities deferred
- **English Only:** All content, interfaces, and documentation in English
- **Time Sensitivity:** Interview links active only within scheduled time window

### Success Criteria
- **Functional Workflow:** Complete interview process from scheduling to feedback
- **User Experience:** Intuitive interfaces for all user roles
- **Technical Reliability:** Robust error handling and graceful degradation
- **Scalable Foundation:** Architecture supports future enhancements

### Key Stakeholders
- **Recruiting Analysts:** Primary users managing interviews and candidates
- **System Administrators:** User management and system configuration
- **Candidates:** Interview participants accessing via unique links
- **Globant Clients:** Indirect beneficiaries of improved hiring process
