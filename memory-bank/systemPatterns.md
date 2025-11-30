# System Patterns

## Architectural Patterns

### 1. Layered Architecture Pattern

**Purpose:**  
Enforce separation of concerns through strict layer boundaries and unidirectional dependencies.

**Layer Structure:**
```
Presentation Layer (FastAPI Routers)
    ↓ (HTTP Requests/Responses)
Business Logic Layer (Services)
    ↓ (Domain Operations)
Data Access Layer (Repositories)
    ↓ (Database Operations)
Data Layer (SQLite + SQLAlchemy Models)
```

**Layer Responsibilities:**

**Routers (Presentation Layer):**
- Handle HTTP semantics only
- Transform requests/responses using Pydantic schemas
- Delegate all business logic to services
- Manage authentication and authorization
- Return appropriate HTTP status codes

**Services (Business Logic Layer):**
- Implement all business rules and validation
- Orchestrate operations across multiple repositories
- Handle complex workflows and transactions
- Integrate with AI agent service when needed
- Transform data between layers

**Repositories (Data Access Layer):**
- Provide clean data access interface
- Execute SQLAlchemy queries and operations
- Handle database-specific concerns
- Return SQLAlchemy model instances
- Manage database sessions properly

**Models (Data Layer):**
- Define database schema and relationships
- Implement data validation constraints
- Provide ORM mapping for SQLAlchemy

**Implementation Expectations:**
- No layer skipping (routers cannot call repositories directly)
- Dependencies flow downward only
- Upper layers depend on abstractions, not implementations
- Each layer has single, well-defined responsibility

### 2. Repository Pattern

**Purpose:**  
Isolate data access logic and provide uniform interface for database operations.

**Responsibilities:**
- Encapsulate all SQLAlchemy query logic
- Provide consistent CRUD operations across entities
- Abstract database technology details
- Enable easy testing through mocking

**Implementation Guidelines:**
1. Inherit from `BaseRepository` class
2. Implement entity-specific query methods
3. Use SQLAlchemy sessions provided via dependency injection
4. Return SQLAlchemy model instances, never Pydantic schemas
5. Raise generic exceptions, not HTTP exceptions

**Expected Methods:**
- `get_by_id(id: int)` - Retrieve single entity
- `get_all(filters: dict)` - Retrieve multiple entities with filtering
- `create(obj_data: dict)` - Create new entity
- `update(id: int, obj_data: dict)` - Update existing entity
- `delete(id: int)` - Delete entity (soft delete preferred)

**Behavioral Expectations:**
- Handle database sessions properly
- Implement proper error handling for DB constraints
- Support filtering and pagination where appropriate
- Maintain transaction boundaries at service layer

### 3. Service Layer Pattern

**Purpose:**  
Encapsulate business logic and coordinate operations between repositories and external services.

**Responsibilities:**
- Implement all business rules and validation
- Coordinate multiple repository operations
- Handle complex business workflows
- Integrate with AI agent service
- Manage transaction boundaries
- Transform between Pydantic schemas and SQLAlchemy models

**Implementation Guidelines:**
1. Receive repositories via dependency injection
2. Validate business rules before data persistence
3. Use Pydantic schemas for input/output
4. Handle all business exceptions appropriately
5. Log important business operations

**Expected Patterns:**
- Input validation using Pydantic schemas
- Business rule enforcement before repository calls
- Proper error handling with meaningful messages
- Transaction management for multi-step operations
- Integration with AI service when domain logic requires it

**Behavioral Expectations:**
- Never execute direct database queries
- Always validate business constraints
- Return clean, processed data to presentation layer
- Handle edge cases gracefully
- Maintain audit trails for important operations

### 4. Dependency Injection Pattern

**Purpose:**  
Manage dependencies and enable testability through inversion of control.

**Implementation Areas:**
- Database session management
- Repository instantiation
- Service layer dependencies
- External service integration

**Guidelines:**
1. Use FastAPI's `Depends()` for dependency injection
2. Create factory functions for complex dependencies
3. Maintain clear dependency hierarchies
4. Enable easy mocking for testing

**Expected Benefits:**
- Loose coupling between layers
- Easy unit testing through mocking
- Consistent dependency management
- Clear separation of concerns

## Design Patterns

### 1. Factory Pattern

**Purpose:**  
Create complex objects with proper validation and configuration.

**Use Cases:**
- AI prompt generation based on interview context
- Interview configuration creation
- Complex entity instantiation with business rules

**Implementation Guidelines:**
1. Create static factory methods for object creation
2. Encapsulate complex initialization logic
3. Validate inputs before object creation
4. Return fully configured, valid objects

**Expected Outcomes:**
- Consistent object creation across the application
- Centralized validation logic
- Reduced code duplication
- Clear object creation patterns

### 2. Strategy Pattern

**Purpose:**  
Enable different algorithms or behaviors to be selected at runtime.

**Use Cases:**
- Different AI interview approaches based on role/seniority
- Multiple validation strategies for different entities
- Various scoring algorithms for interview evaluation

**Implementation Guidelines:**
1. Define abstract strategy interface
2. Implement concrete strategies for each variation
3. Use context class to manage strategy selection
4. Enable runtime strategy switching

**Expected Benefits:**
- Flexible behavior modification
- Easy addition of new strategies
- Clean separation of algorithm variations
- Testable individual strategies

### 3. Observer Pattern

**Purpose:**  
Enable event-driven updates and notifications across the system.

**Use Cases:**
- Interview status change notifications
- Audit logging for important events
- Real-time updates for frontend clients

**Implementation Guidelines:**
1. Define observer interface for event handling
2. Implement concrete observers for specific actions
3. Use subject class to manage observer registration
4. Ensure proper event notification ordering

**Expected Behaviors:**
- Loose coupling between event producers and consumers
- Scalable event handling system
- Consistent notification patterns
- Proper error isolation in observers

### 4. Adapter Pattern

**Purpose:**  
Integrate external services and transform data between different interfaces.

**Use Cases:**
- AI service integration with different providers
- File storage abstraction for different backends
- External API integration

**Implementation Guidelines:**
1. Create adapter interface for external service
2. Implement concrete adapters for each provider
3. Transform external data to internal formats
4. Handle external service failures gracefully

**Expected Outcomes:**
- Clean integration with external services
- Easy switching between service providers
- Consistent internal data formats
- Isolated external dependencies

## Frontend Patterns

### 1. Composition Pattern (Vue 3)

**Purpose:**  
Build reusable, modular components through composition rather than inheritance.

**Implementation Guidelines:**
1. Use Vue 3 Composition API with `<script setup>`
2. Create focused composables for specific functionality
3. Combine simple components to build complex UIs
4. Leverage props and slots for component flexibility

**Expected Composables:**
- `useAuth()` - Authentication state and operations
- `useApi()` - API request handling with loading/error states
- `useValidation()` - Form validation logic
- `usePagination()` - List pagination functionality

**Behavioral Expectations:**
- Components remain small and focused
- Logic is reusable across different components
- Clear separation between UI and business logic
- Consistent patterns across all composables

### 2. State Management Pattern (Pinia)

**Purpose:**  
Centralize application state and provide predictable state mutations.

**Store Structure Guidelines:**
1. Organize stores by domain (auth, candidates, interviews)
2. Use reactive state with computed getters
3. Implement async actions for API calls
4. Maintain minimal, normalized state

**Expected Store Patterns:**
- State: Reactive data properties
- Getters: Computed derived state
- Actions: Async operations and state mutations
- Proper error handling in all actions

**Behavioral Expectations:**
- Single source of truth for each domain
- Predictable state updates
- Proper loading and error state management
- Clean separation between stores

### 3. Component Communication Pattern

**Purpose:**  
Establish clear communication patterns between Vue components.

**Communication Rules:**
- Parent to Child: Props
- Child to Parent: Events (`emit`)
- Global State: Pinia stores
- Sibling Components: Shared store or parent coordination

**Implementation Guidelines:**
1. Define clear prop interfaces with TypeScript
2. Use descriptive event names
3. Avoid deep prop drilling
4. Leverage provide/inject for deep component trees

**Expected Behaviors:**
- Unidirectional data flow
- Clear component boundaries
- Minimal coupling between components
- Predictable data updates

## Error Handling Patterns

### 1. Centralized Error Handling

**Purpose:**  
Provide consistent error handling and user feedback across the application.

**Backend Error Handling:**
- Service layer validates business rules
- Repositories handle database constraints
- Global exception handler manages HTTP responses
- Structured error logging for debugging

**Frontend Error Handling:**
- API service handles HTTP errors
- Components display user-friendly messages
- Global error boundary for unhandled errors
- Consistent error message formatting

**Implementation Guidelines:**
1. Define error types and corresponding HTTP status codes
2. Create user-friendly error messages
3. Log errors with sufficient context
4. Provide recovery options where possible

**Expected Outcomes:**
- Consistent error experience across application
- Proper error logging for debugging
- Graceful degradation on failures
- Clear user guidance on error resolution

### 2. Graceful Degradation Pattern

**Purpose:**  
Maintain application functionality when external services fail.

**Implementation Areas:**
- AI service fallbacks for interview generation
- Offline functionality for critical features
- Default values for missing configuration
- Alternative workflows when services unavailable

**Guidelines:**
1. Identify critical vs. non-critical functionality
2. Implement fallback mechanisms for external dependencies
3. Provide meaningful feedback when features unavailable
4. Maintain core functionality during partial failures

**Expected Behaviors:**
- Application remains usable during service outages
- Users receive clear feedback about unavailable features
- Critical workflows have backup options
- System recovers automatically when services restore

## Security Patterns

### 1. Authentication Middleware

**Purpose:**  
Centralize authentication logic and ensure consistent security enforcement.

**Implementation Guidelines:**
1. Use JWT tokens for stateless authentication
2. Implement token validation middleware
3. Provide user context to protected endpoints
4. Handle token expiration gracefully

**Expected Security Features:**
- Secure token generation and validation
- Proper session management
- Protection against common attacks (CSRF, XSS)
- Audit logging for authentication events

### 2. Authorization Pattern

**Purpose:**  
Implement role-based access control throughout the application.

**Implementation Guidelines:**
1. Define clear role hierarchy
2. Use decorators for endpoint protection
3. Implement permission checking at service layer
4. Provide clear feedback for unauthorized access

**Expected Behaviors:**
- Consistent permission enforcement
- Clear role-based access patterns
- Proper error handling for unauthorized requests
- Audit trails for permission violations

## Performance Patterns

### 1. Caching Strategy

**Purpose:**  
Improve application performance through strategic data caching.

**Caching Areas:**
- Lookup data (roles, seniorities, clients)
- User session information
- Frequently accessed interview data
- AI prompt templates

**Implementation Guidelines:**
1. Identify cacheable data with low change frequency
2. Implement appropriate cache invalidation strategies
3. Use memory caching for frequently accessed data
4. Monitor cache hit rates and effectiveness

**Expected Outcomes:**
- Reduced database query load
- Improved response times
- Efficient resource utilization
- Scalable performance characteristics

### 2. Lazy Loading Pattern

**Purpose:**  
Load data and components only when needed to improve initial load times.

**Implementation Areas:**
- Vue route components
- Large data sets with pagination
- Optional component features
- Heavy computational operations

**Guidelines:**
1. Implement route-level code splitting
2. Use pagination for large data sets
3. Load optional features on demand
4. Provide loading indicators for async operations

**Expected Benefits:**
- Faster initial application load
- Reduced memory usage
- Better user experience
- Efficient resource utilization

## Integration Patterns

### 1. API Gateway Pattern

**Purpose:**  
Provide centralized API management and consistent routing.

**Implementation Guidelines:**
1. Use FastAPI router system for endpoint organization
2. Implement global middleware for cross-cutting concerns
3. Provide consistent API versioning
4. Enable centralized logging and monitoring

**Expected Features:**
- Consistent API structure across all endpoints
- Global error handling and logging
- Proper CORS configuration
- API documentation generation

### 2. Circuit Breaker Pattern

**Purpose:**  
Prevent cascading failures when external services become unavailable.

**Implementation Areas:**
- AI service integration
- External API calls
- Database connection handling
- File storage operations

**Guidelines:**
1. Define failure thresholds for each external service
2. Implement automatic recovery mechanisms
3. Provide fallback responses during outages
4. Monitor service health and availability

**Expected Behaviors:**
- Automatic failure detection and isolation
- Graceful degradation during service outages
- Automatic recovery when services restore
- Proper monitoring and alerting

## Data Access Patterns

### 1. Unit of Work Pattern

**Purpose:**  
Manage complex transactions involving multiple repositories.

**Implementation Guidelines:**
1. Coordinate multiple repository operations
2. Ensure transaction consistency
3. Handle rollback scenarios properly
4. Maintain clear transaction boundaries

**Expected Behaviors:**
- Atomic operations across multiple entities
- Proper error handling and rollback
- Clear transaction scope definition
- Consistent data state management

### 2. Specification Pattern

**Purpose:**  
Encapsulate business rules and query logic in reusable components.

**Implementation Guidelines:**
1. Define specification interface for business rules
2. Implement concrete specifications for different criteria
3. Enable specification composition for complex queries
4. Support both in-memory and database filtering

**Expected Outcomes:**
- Reusable business rule definitions
- Flexible query composition
- Testable business logic
- Consistent filtering patterns

## Testing Patterns

### 1. Test Data Builder Pattern

**Purpose:**  
Create test data with fluent, readable interfaces.

**Implementation Guidelines:**
1. Create builder classes for each entity
2. Provide fluent methods for data customization
3. Include sensible defaults for all fields
4. Enable easy test data variation

**Expected Benefits:**
- Readable and maintainable test code
- Easy test data creation and modification
- Consistent test data patterns
- Reduced test setup complexity

### 2. Mock Pattern

**Purpose:**  
Isolate units under test by mocking external dependencies.

**Implementation Guidelines:**
1. Mock external services (AI, file storage)
2. Mock repository layers for service testing
3. Provide predictable mock responses
4. Verify mock interactions in tests

**Expected Outcomes:**
- Fast, isolated unit tests
- Predictable test behavior
- Easy testing of error scenarios
- Clear test boundaries

## Monitoring and Logging Patterns

### 1. Structured Logging

**Purpose:**  
Provide consistent, searchable log format for debugging and monitoring.

**Implementation Guidelines:**
1. Use structured log format (JSON)
2. Include relevant context in all log entries
3. Implement consistent log levels
4. Enable log aggregation and searching

**Expected Log Categories:**
- Business operation logs (interview start/completion)
- AI service interaction logs
- Error and exception logs
- Performance and timing logs

### 2. Health Check Pattern

**Purpose:**  
Monitor system health and dependency availability.

**Implementation Guidelines:**
1. Implement health checks for all critical dependencies
2. Provide detailed health status information
3. Enable automated monitoring and alerting
4. Include performance metrics in health reports

**Expected Health Checks:**
- Database connectivity and performance
- AI service availability and response time
- File storage accessibility
- External API availability

These patterns provide the foundation for building a maintainable, scalable, and robust AI interview system while following established software engineering best practices and the project's specific architectural requirements.
