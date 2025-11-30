# System Patterns

## Architectural Patterns

### 1. Layered Architecture Pattern
The system follows a strict layered architecture to ensure separation of concerns and maintainability:

**Backend Layers:**
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
- **Routers:** Handle HTTP semantics, request/response transformation, authentication
- **Services:** Implement business logic, orchestrate operations, validate business rules
- **Repositories:** Provide data access abstraction, execute database operations
- **Models:** Define data structure and relationships

**Layer Interaction Rules:**
- Each layer can only communicate with the layer directly below it
- No layer skipping allowed (e.g., routers cannot call repositories directly)
- Dependencies flow downward only
- Upper layers depend on abstractions, not concrete implementations

### 2. Repository Pattern
Encapsulates data access logic and provides a uniform interface for data operations:

**Implementation:**
```python
# Abstract base repository
class BaseRepository:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_by_id(self, id: int):
        pass
    
    async def create(self, obj_data):
        pass
    
    async def update(self, id: int, obj_data):
        pass
    
    async def delete(self, id: int):
        pass

# Concrete implementation
class CandidateRepository(BaseRepository):
    async def get_by_id(self, id: int):
        return self.db.query(Candidate).filter(Candidate.id == id).first()
```

**Benefits:**
- Centralized data access logic
- Easy testing through mocking
- Consistent data operations across entities
- Database technology abstraction

### 3. Service Layer Pattern
Encapsulates business logic and coordinates between different repositories:

**Implementation:**
```python
class InterviewService:
    def __init__(self, 
                 interview_repo: InterviewRepository,
                 candidate_repo: CandidateRepository,
                 ai_service: AIAgentService):
        self.interview_repo = interview_repo
        self.candidate_repo = candidate_repo
        self.ai_service = ai_service
    
    async def create_interview(self, interview_data):
        # Business logic validation
        # Coordinate multiple repositories
        # Return business objects
```

**Responsibilities:**
- Implement business rules and validation
- Coordinate multiple repositories
- Handle complex business operations
- Manage transactions and data consistency

### 4. Dependency Injection Pattern
Used throughout the system to manage dependencies and enable testability:

**FastAPI Implementation:**
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_interview_service(db: Session = Depends(get_db)):
    interview_repo = InterviewRepository(db)
    candidate_repo = CandidateRepository(db)
    ai_service = AIAgentService()
    return InterviewService(interview_repo, candidate_repo, ai_service)

@router.post("/interviews")
async def create_interview(
    interview_data: InterviewCreate,
    service: InterviewService = Depends(get_interview_service)
):
    return await service.create_interview(interview_data)
```

## Design Patterns

### 1. Factory Pattern
Used for creating complex objects with validation and configuration:

**AI Prompt Factory:**
```python
class AIPromptFactory:
    @staticmethod
    def create_interview_prompt(job_description: str, cv_content: str, guidelines: str):
        return InterviewPrompt(
            introduction=PromptTemplates.INTRODUCTION,
            job_context=job_description,
            candidate_background=cv_content,
            specific_guidelines=guidelines,
            evaluation_criteria=PromptTemplates.EVALUATION_CRITERIA
        )
```

**Interview Configuration Factory:**
```python
class InterviewConfigFactory:
    @staticmethod
    def create_config(interview_data: dict):
        # Validate data
        # Set defaults
        # Create configuration object
        return InterviewConfiguration(**validated_data)
```

### 2. Strategy Pattern
Used for different AI interview approaches and business logic variations:

**AI Interview Strategy:**
```python
class InterviewStrategy(ABC):
    @abstractmethod
    async def conduct_interview(self, config: InterviewConfig):
        pass

class TechnicalInterviewStrategy(InterviewStrategy):
    async def conduct_interview(self, config: InterviewConfig):
        # Technical interview logic
        pass

class SeniorLevelInterviewStrategy(InterviewStrategy):
    async def conduct_interview(self, config: InterviewConfig):
        # Senior-level specific questions
        pass

class InterviewContext:
    def __init__(self, strategy: InterviewStrategy):
        self.strategy = strategy
    
    async def execute_interview(self, config: InterviewConfig):
        return await self.strategy.conduct_interview(config)
```

**Validation Strategy:**
```python
class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, data):
        pass

class CandidateValidationStrategy(ValidationStrategy):
    def validate(self, candidate_data):
        # Candidate-specific validation
        pass

class InterviewValidationStrategy(ValidationStrategy):
    def validate(self, interview_data):
        # Interview-specific validation
        pass
```

### 3. Observer Pattern
Used for event-driven updates and notifications:

**Interview Status Observer:**
```python
class InterviewStatusObserver(ABC):
    @abstractmethod
    async def on_status_change(self, interview_id: int, old_status: str, new_status: str):
        pass

class NotificationObserver(InterviewStatusObserver):
    async def on_status_change(self, interview_id: int, old_status: str, new_status: str):
        # Send notifications
        pass

class AuditObserver(InterviewStatusObserver):
    async def on_status_change(self, interview_id: int, old_status: str, new_status: str):
        # Log status changes
        pass

class InterviewStatusSubject:
    def __init__(self):
        self.observers = []
    
    def attach(self, observer: InterviewStatusObserver):
        self.observers.append(observer)
    
    async def notify_status_change(self, interview_id: int, old_status: str, new_status: str):
        for observer in self.observers:
            await observer.on_status_change(interview_id, old_status, new_status)
```

### 4. Adapter Pattern
Used for external service integration and data transformation:

**AI Service Adapter:**
```python
class AIServiceAdapter:
    def __init__(self, external_ai_client):
        self.client = external_ai_client
    
    async def conduct_interview(self, prompt: str) -> InterviewResponse:
        # Adapt external AI response to internal format
        external_response = await self.client.generate_response(prompt)
        return self._adapt_response(external_response)
    
    def _adapt_response(self, external_response) -> InterviewResponse:
        # Transform external format to internal format
        pass
```

**File Storage Adapter:**
```python
class FileStorageAdapter:
    def __init__(self, storage_provider):
        self.provider = storage_provider
    
    async def store_file(self, file_data: bytes, filename: str) -> str:
        # Adapt to different storage providers
        return await self.provider.upload(file_data, filename)
```

## Frontend Patterns

### 1. Composition Pattern
Vue 3 Composition API for component reusability:

**Composables:**
```javascript
// useAuth.js
export function useAuth() {
    const user = ref(null)
    const isAuthenticated = computed(() => !!user.value)
    
    const login = async (credentials) => {
        // Authentication logic
    }
    
    const logout = () => {
        // Logout logic
    }
    
    return {
        user: readonly(user),
        isAuthenticated,
        login,
        logout
    }
}

// useApi.js
export function useApi() {
    const loading = ref(false)
    const error = ref(null)
    
    const request = async (apiCall) => {
        loading.value = true
        error.value = null
        try {
            const result = await apiCall()
            return result
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }
    
    return {
        loading: readonly(loading),
        error: readonly(error),
        request
    }
}
```

### 2. State Management Pattern
Pinia store pattern for centralized state management:

**Store Structure:**
```javascript
// stores/interviews.js
export const useInterviewStore = defineStore('interviews', () => {
    const interviews = ref([])
    const currentInterview = ref(null)
    const loading = ref(false)
    
    const fetchInterviews = async (filters = {}) => {
        loading.value = true
        try {
            const response = await api.getInterviews(filters)
            interviews.value = response.data
        } finally {
            loading.value = false
        }
    }
    
    const createInterview = async (interviewData) => {
        const response = await api.createInterview(interviewData)
        interviews.value.push(response.data)
        return response.data
    }
    
    return {
        interviews: readonly(interviews),
        currentInterview: readonly(currentInterview),
        loading: readonly(loading),
        fetchInterviews,
        createInterview
    }
})
```

### 3. Component Communication Pattern
Structured communication between Vue components:

**Props Down, Events Up:**
```vue
<!-- Parent Component -->
<template>
    <CandidateList 
        :candidates="candidates"
        :loading="loading"
        @candidate-selected="handleCandidateSelection"
        @filter-changed="handleFilterChange"
    />
</template>

<!-- Child Component -->
<template>
    <div>
        <div v-for="candidate in candidates" :key="candidate.id">
            <button @click="selectCandidate(candidate)">
                {{ candidate.name }}
            </button>
        </div>
    </div>
</template>

<script setup>
const props = defineProps(['candidates', 'loading'])
const emit = defineEmits(['candidate-selected', 'filter-changed'])

const selectCandidate = (candidate) => {
    emit('candidate-selected', candidate)
}
</script>
```

## Error Handling Patterns

### 1. Centralized Error Handling
Consistent error handling across the application:

**Backend Error Handler:**
```python
class ErrorHandler:
    @staticmethod
    def handle_service_error(error: Exception) -> HTTPException:
        if isinstance(error, ValidationError):
            return HTTPException(status_code=400, detail=str(error))
        elif isinstance(error, NotFoundError):
            return HTTPException(status_code=404, detail=str(error))
        elif isinstance(error, AuthenticationError):
            return HTTPException(status_code=401, detail=str(error))
        else:
            logger.error(f"Unexpected error: {error}")
            return HTTPException(status_code=500, detail="Internal server error")

# Usage in routers
@router.post("/interviews")
async def create_interview(interview_data: InterviewCreate, service: InterviewService = Depends()):
    try:
        return await service.create_interview(interview_data)
    except Exception as e:
        raise ErrorHandler.handle_service_error(e)
```

**Frontend Error Handler:**
```javascript
// utils/errorHandler.js
export class ErrorHandler {
    static handle(error) {
        if (error.response) {
            // Server responded with error status
            const status = error.response.status
            const message = error.response.data.detail || 'An error occurred'
            
            switch (status) {
                case 400:
                    return { type: 'validation', message }
                case 401:
                    return { type: 'authentication', message }
                case 404:
                    return { type: 'not_found', message }
                default:
                    return { type: 'server', message }
            }
        } else if (error.request) {
            // Network error
            return { type: 'network', message: 'Network error occurred' }
        } else {
            // Other error
            return { type: 'unknown', message: error.message }
        }
    }
}
```

### 2. Graceful Degradation Pattern
Handle service failures gracefully:

**AI Service Fallback:**
```python
class AIServiceWithFallback:
    def __init__(self, primary_service, fallback_service):
        self.primary = primary_service
        self.fallback = fallback_service
    
    async def conduct_interview(self, prompt: str):
        try:
            return await self.primary.conduct_interview(prompt)
        except AIServiceException:
            logger.warning("Primary AI service failed, using fallback")
            return await self.fallback.conduct_interview(prompt)
        except Exception:
            logger.error("Both AI services failed")
            return self._create_fallback_response()
    
    def _create_fallback_response(self):
        return InterviewResponse(
            message="Interview service temporarily unavailable",
            status="error"
        )
```

## Security Patterns

### 1. Authentication Middleware Pattern
Centralized authentication handling:

**JWT Authentication Middleware:**
```python
class JWTAuthMiddleware:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    async def authenticate(self, token: str) -> User:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id = payload.get("sub")
            if user_id is None:
                raise AuthenticationError("Invalid token")
            return await self.get_user(user_id)
        except JWTError:
            raise AuthenticationError("Invalid token")

# FastAPI dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    auth_middleware = JWTAuthMiddleware(settings.SECRET_KEY)
    return await auth_middleware.authenticate(token)
```

### 2. Authorization Pattern
Role-based access control:

**Permission Decorator:**
```python
def require_permission(required_role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user or current_user.role != required_role:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@require_permission("admin")
async def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    # Admin-only operation
    pass
```

## Performance Patterns

### 1. Caching Pattern
Strategic caching for improved performance:

**Repository Caching:**
```python
class CachedLookupRepository:
    def __init__(self, base_repo: LookupRepository, cache_ttl: int = 3600):
        self.base_repo = base_repo
        self.cache = {}
        self.cache_ttl = cache_ttl
    
    async def get_by_domain(self, domain: str):
        cache_key = f"lookup_{domain}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
        
        data = await self.base_repo.get_by_domain(domain)
        self.cache[cache_key] = (data, time.time())
        return data
```

### 2. Lazy Loading Pattern
Load data only when needed:

**Frontend Lazy Loading:**
```javascript
// Lazy route loading
const routes = [
    {
        path: '/interviews',
        component: () => import('../views/InterviewsView.vue')
    },
    {
        path: '/candidates',
        component: () => import('../views/CandidatesView.vue')
    }
]

// Lazy data loading composable
export function useLazyData(fetchFunction) {
    const data = ref(null)
    const loading = ref(false)
    const loaded = ref(false)
    
    const load = async () => {
        if (loaded.value) return data.value
        
        loading.value = true
        try {
            data.value = await fetchFunction()
            loaded.value = true
        } finally {
            loading.value = false
        }
        return data.value
    }
    
    return { data: readonly(data), loading: readonly(loading), load }
}
```

**Backend Lazy Loading:**
```python
class LazyLoadedRepository:
    def __init__(self, db: Session):
        self.db = db
        self._cache = {}
    
    async def get_with_relations(self, id: int, include_relations: bool = False):
        base_query = self.db.query(Interview).filter(Interview.id == id)
        
        if include_relations:
            # Only load relations when explicitly requested
            base_query = base_query.options(
                joinedload(Interview.candidate),
                joinedload(Interview.analyst),
                joinedload(Interview.feedback)
            )
        
        return base_query.first()
```

## Integration Patterns

### 1. API Gateway Pattern
Centralized API management and routing:

**API Router Configuration:**
```python
# main.py
app = FastAPI(title="Interview System API", version="1.0.0")

# Include all routers with common prefix
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(candidates_router, prefix="/api/v1/candidates", tags=["candidates"])
app.include_router(interviews_router, prefix="/api/v1/interviews", tags=["interviews"])
app.include_router(lookup_router, prefix="/api/v1/lookup", tags=["lookup"])

# Global middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return ErrorHandler.handle_global_error(exc)
```

### 2. Circuit Breaker Pattern
Prevent cascading failures in external service calls:

**AI Service Circuit Breaker:**
```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenException("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        self.failure_count = 0
        self.state = "CLOSED"
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

class AIServiceWithCircuitBreaker:
    def __init__(self, ai_service):
        self.ai_service = ai_service
        self.circuit_breaker = CircuitBreaker()
    
    async def conduct_interview(self, prompt: str):
        return await self.circuit_breaker.call(
            self.ai_service.conduct_interview, 
            prompt
        )
```

## Data Access Patterns

### 1. Unit of Work Pattern
Manage transactions and coordinate multiple repositories:

**Unit of Work Implementation:**
```python
class UnitOfWork:
    def __init__(self, db: Session):
        self.db = db
        self.interview_repo = InterviewRepository(db)
        self.candidate_repo = CandidateRepository(db)
        self.feedback_repo = FeedbackRepository(db)
        self.transcript_repo = TranscriptRepository(db)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
    
    async def commit(self):
        self.db.commit()
    
    async def rollback(self):
        self.db.rollback()

# Usage
async def complete_interview_workflow(interview_id: int, transcript: str, feedback: dict):
    async with UnitOfWork(db) as uow:
        # Update interview status
        interview = await uow.interview_repo.get_by_id(interview_id)
        interview.status = "completed"
        await uow.interview_repo.update(interview)
        
        # Save transcript
        await uow.transcript_repo.create({
            "interview_id": interview_id,
            "content": transcript
        })
        
        # Save feedback
        await uow.feedback_repo.create({
            "interview_id": interview_id,
            **feedback
        })
        
        # All operations committed together
```

### 2. Specification Pattern
Encapsulate business rules and query logic:

**Specification Implementation:**
```python
class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate) -> bool:
        pass
    
    @abstractmethod
    def to_sql_criteria(self):
        pass

class CandidateByRoleSpecification(Specification):
    def __init__(self, role_id: int):
        self.role_id = role_id
    
    def is_satisfied_by(self, candidate) -> bool:
        return any(interview.role_id == self.role_id for interview in candidate.interviews)
    
    def to_sql_criteria(self):
        return Interview.role_id == self.role_id

class ActiveCandidateSpecification(Specification):
    def is_satisfied_by(self, candidate) -> bool:
        return candidate.is_active
    
    def to_sql_criteria(self):
        return Candidate.is_active == True

class CompositeSpecification(Specification):
    def __init__(self, *specifications):
        self.specifications = specifications
    
    def is_satisfied_by(self, candidate) -> bool:
        return all(spec.is_satisfied_by(candidate) for spec in self.specifications)
    
    def to_sql_criteria(self):
        criteria = [spec.to_sql_criteria() for spec in self.specifications]
        return and_(*criteria)

# Usage
active_candidates_for_role = CompositeSpecification(
    ActiveCandidateSpecification(),
    CandidateByRoleSpecification(role_id=1)
)

filtered_candidates = db.query(Candidate).filter(
    active_candidates_for_role.to_sql_criteria()
).all()
```

## Testing Patterns

### 1. Test Data Builder Pattern
Create test data with fluent interface:

**Test Data Builders:**
```python
class CandidateBuilder:
    def __init__(self):
        self.data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "id_document": "12345678",
            "is_active": True
        }
    
    def with_name(self, first_name: str, last_name: str):
        self.data["first_name"] = first_name
        self.data["last_name"] = last_name
        return self
    
    def with_email(self, email: str):
        self.data["email"] = email
        return self
    
    def inactive(self):
        self.data["is_active"] = False
        return self
    
    def build(self) -> dict:
        return self.data.copy()

class InterviewBuilder:
    def __init__(self):
        self.data = {
            "analyst_id": 1,
            "candidate_id": 1,
            "role_id": 1,
            "seniority_id": 1,
            "scheduled_datetime": "2024-01-01T10:00:00",
            "status_id": 1
        }
    
    def for_candidate(self, candidate_id: int):
        self.data["candidate_id"] = candidate_id
        return self
    
    def with_role(self, role_id: int):
        self.data["role_id"] = role_id
        return self
    
    def scheduled_for(self, datetime_str: str):
        self.data["scheduled_datetime"] = datetime_str
        return self
    
    def build(self) -> dict:
        return self.data.copy()

# Usage in tests
def test_create_interview():
    candidate_data = CandidateBuilder().with_name("Jane", "Smith").build()
    interview_data = InterviewBuilder().for_candidate(1).with_role(2).build()
    
    # Test logic here
```

### 2. Mock Pattern
Mock external dependencies for isolated testing:

**AI Service Mock:**
```python
class MockAIService:
    def __init__(self):
        self.responses = {}
        self.call_count = 0
    
    def set_response(self, prompt_key: str, response: dict):
        self.responses[prompt_key] = response
    
    async def conduct_interview(self, prompt: str) -> dict:
        self.call_count += 1
        # Return predefined response based on prompt content
        for key, response in self.responses.items():
            if key in prompt:
                return response
        
        # Default response
        return {
            "message": "Mock interview response",
            "feedback": {"overall_ranking": 3}
        }

# Usage in tests
@pytest.fixture
def mock_ai_service():
    mock = MockAIService()
    mock.set_response("Python", {
        "message": "Good Python knowledge",
        "feedback": {"overall_ranking": 4}
    })
    return mock

async def test_interview_service_with_mock(mock_ai_service):
    service = InterviewService(
        interview_repo=mock_interview_repo,
        ai_service=mock_ai_service
    )
    
    result = await service.conduct_interview(interview_id=1)
    assert mock_ai_service.call_count == 1
    assert result["feedback"]["overall_ranking"] == 4
```

## Monitoring and Logging Patterns

### 1. Structured Logging Pattern
Consistent, searchable log format:

**Structured Logger:**
```python
import structlog

logger = structlog.get_logger()

class StructuredLogger:
    @staticmethod
    def log_interview_start(interview_id: int, candidate_id: int):
        logger.info(
            "interview_started",
            interview_id=interview_id,
            candidate_id=candidate_id,
            timestamp=datetime.utcnow().isoformat()
        )
    
    @staticmethod
    def log_ai_request(interview_id: int, prompt_length: int, response_time: float):
        logger.info(
            "ai_request_completed",
            interview_id=interview_id,
            prompt_length=prompt_length,
            response_time_ms=response_time * 1000,
            timestamp=datetime.utcnow().isoformat()
        )
    
    @staticmethod
    def log_error(error: Exception, context: dict):
        logger.error(
            "application_error",
            error_type=type(error).__name__,
            error_message=str(error),
            context=context,
            timestamp=datetime.utcnow().isoformat()
        )
```

### 2. Health Check Pattern
Monitor system health and dependencies:

**Health Check Implementation:**
```python
class HealthChecker:
    def __init__(self, db: Session, ai_service: AIService):
        self.db = db
        self.ai_service = ai_service
    
    async def check_database(self) -> dict:
        try:
            # Simple query to test database connectivity
            result = self.db.execute("SELECT 1").fetchone()
            return {"status": "healthy", "response_time": "< 1ms"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    async def check_ai_service(self) -> dict:
        try:
            start_time = time.time()
            await self.ai_service.health_check()
            response_time = (time.time() - start_time) * 1000
            return {"status": "healthy", "response_time": f"{response_time:.2f}ms"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    async def get_health_status(self) -> dict:
        checks = {
            "database": await self.check_database(),
            "ai_service": await self.check_ai_service()
        }
        
        overall_status = "healthy" if all(
            check["status"] == "healthy" for check in checks.values()
        ) else "unhealthy"
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": checks
        }

# FastAPI endpoint
@router.get("/health")
async def health_check(health_checker: HealthChecker = Depends()):
    return await health_checker.get_health_status()
```

These patterns provide a comprehensive foundation for building a maintainable, scalable, and robust AI interview system while following established software engineering best practices.
