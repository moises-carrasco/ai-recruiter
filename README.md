# AI Technical Interview System - Globant

An AI-powered web application that conducts technical interviews with Globant workers (Globers) applying for specific positions within client accounts. The system replaces manual initial technical screenings with automated, objective AI-driven conversations focused on quantifiable technical competencies.

## 🎯 Project Overview

### Core Value Proposition
- **Automated Technical Screening**: Replace manual interviews with AI-conducted conversations
- **Objective Assessment**: Focus exclusively on measurable technical attributes
- **Standardized Process**: Ensure consistent evaluation criteria across all interviews
- **Scalable Solution**: Handle multiple interviews simultaneously without resource constraints

### Key Features
- 🤖 **AI-Driven Interviews**: Conversational technical assessments based on Job Descriptions and CVs
- 📊 **Structured Feedback**: 1-5 ranking system with detailed skill evaluations
- 👥 **Role-Based Access**: Admin, Recruiting Analyst, and Candidate user roles
- 📁 **File Management**: Upload and storage of CVs and Job Descriptions
- 🔗 **Secure Links**: Time-sensitive interview links for candidate access
- 📋 **CRUD Operations**: Complete management of candidates, interviews, and users
- 🎯 **Objective Evaluation**: Focus on quantifiable technical skills only

## 📁 Documentation

The project includes comprehensive documentation in the `docs/` folder:

- **📋 Backlog & User Stories**: Complete user stories and requirements (`docs/backlog - user_stories.md`)
- **📝 Project Definition**: Detailed project scope and objectives (`docs/project definition.md`)
- **🎨 Design Mockups**: UI/UX design references and wireframes (`docs/mockups/`)
- **📄 Sample Documents**: Example CVs and job descriptions for testing (`docs/candidate_cv_jd_samples/`)

These resources provide guidance for development, testing, and understanding the project requirements.

## 🏗️ Architecture & Technology Stack

### Backend Architecture
```
API Layer (FastAPI Routes)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Data Access)
    ↓
Database Layer (SQLite)
```

**Technology Stack:**
- **Framework**: FastAPI (Python async web framework)
- **ORM**: SQLAlchemy 2.0 with async support
- **Database**: SQLite (with PostgreSQL migration path)
- **Validation**: Pydantic v2
- **Authentication**: JWT tokens with bcrypt password hashing
- **AI Integration**: External AI service (OpenAI API compatible)
- **HTTP Client**: httpx for async AI API calls
- **File Handling**: aiofiles for async file operations

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

**Technology Stack:**
- **Framework**: Vue 3 with Composition API
- **Build Tool**: Vite
- **Routing**: Vue Router 4
- **State Management**: Pinia (Vue 3 store)
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios with custom timeout configuration
- **Development**: ESLint, Prettier

### Database Schema
**Core Entities:**
- **Users**: Admin, Recruiting Analysts with role-based permissions
- **Candidates**: Globant workers applying for positions
- **Interviews**: Scheduled technical assessments with AI
- **Interview Transcripts**: Complete conversation logs
- **Interview Feedback**: Structured evaluation results
- **Lookup Tables**: Roles, Seniorities, Clients, Statuses

**Key Relationships:**
- Users create Interviews
- Candidates participate in Interviews
- Interviews have associated Transcripts and Feedback
- Interviews link to Roles, Seniorities, and Clients

## 🚀 Quick Start

### Prerequisites
- **Python**: 3.10
- **Node.js**: 18.0 or higher
- **SQLite**: 3.x (usually pre-installed)
- **Git**: For version control

### Backend Setup

1. **Clone and navigate to backend:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration:**
   Create a `.env` file in the `backend/` directory:
   ```bash
   # Database
   DATABASE_URL=sqlite:///./interview_system.db

   # Security
   SECRET_KEY=your-super-secret-key-here-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # AI Service Configuration
   # IMPORTANT: Place your AI assistant URL and token here
   AI_API_URL=https://api.openai.com/v1/chat/completions
   AI_AUTH_TOKEN=your-ai-auth-token-here

   # File Upload Configuration
   MAX_UPLOAD_SIZE=10485760  # 10MB in bytes
   ALLOWED_EXTENSIONS=txt,md
   ```

5. **Initialize database:**
   ```bash
   python -m app.db.init_db
   ```

6. **Run backend server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Environment configuration:**
   Create a `.env` file in the frontend directory:
   ```bash
   VITE_API_BASE_URL=http://localhost:8000/api/v1
   ```

4. **Run development server:**
   ```bash
   npm run dev
   ```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)

## 📋 Dependencies

### Backend Dependencies (requirements.txt)
```txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database & ORM
sqlalchemy==2.0.23
alembic==1.12.1

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Data Validation
pydantic==2.5.0
pydantic-settings==2.1.0

# AI Integration
openai==1.3.7
httpx==0.25.2

# Development & Testing
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
flake8==6.1.0

# Environment & Utils
python-dotenv==1.0.0
aiofiles==23.2.1
```

### Frontend Dependencies (package.json)
```json
{
  "dependencies": {
    "vue": "^3.3.8",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.6",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "eslint": "^8.54.0",
    "eslint-plugin-vue": "^9.18.1",
    "prettier": "^3.1.0",
    "@vue/eslint-config-prettier": "^8.0.0"
  }
}
```

## 📁 Project Structure

### Backend Structure
```
backend/
├── app/
│   ├── api/v1/routes/          # API endpoint definitions
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── users.py           # User management
│   │   ├── candidates.py      # Candidate CRUD
│   │   ├── interviews.py      # Interview management & chat
│   │   └── lookup.py          # Lookup table management
│   ├── core/                  # Core configuration
│   │   ├── config.py          # Environment & app config
│   │   ├── security.py        # JWT & password utilities
│   │   └── logging_config.py  # Logging setup
│   ├── models/                # SQLAlchemy models
│   │   ├── base.py            # Base model class
│   │   ├── user.py            # User model
│   │   ├── candidate.py       # Candidate model
│   │   ├── interview.py       # Interview model
│   │   └── lookup.py          # Lookup table models
│   ├── schemas/               # Pydantic schemas
│   │   ├── auth.py            # Authentication schemas
│   │   ├── user.py            # User validation
│   │   ├── candidate.py       # Candidate validation
│   │   ├── interview.py       # Interview validation
│   │   └── lookup.py          # Lookup validation
│   ├── services/              # Business logic layer
│   │   ├── auth_service.py    # Authentication logic
│   │   ├── user_service.py    # User operations
│   │   ├── candidate_service.py # Candidate operations
│   │   ├── interview_service.py # Interview & chat logic
│   │   ├── lookup_service.py  # Lookup operations
│   │   └── ai_agent_service.py # AI integration
│   ├── repositories/          # Data access layer
│   │   ├── base.py            # Base repository
│   │   ├── user_repo.py       # User data access
│   │   ├── candidate_repo.py  # Candidate data access
│   │   ├── interview_repo.py  # Interview data access
│   │   └── lookup_repo.py     # Lookup data access
│   ├── utils/                 # Utility functions
│   │   ├── file_handler.py    # File upload utilities
│   │   └── link_generator.py  # Interview link generation
│   ├── db/                    # Database utilities
│   │   ├── session.py         # Database session management
│   │   └── init_db.py         # Database initialization
│   └── main.py                # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── test_ai.py                # AI service testing script
└── README.md                 # Backend documentation
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/            # Reusable Vue components
│   │   ├── common/           # Shared components (NavigationBar, LoadingSpinner, etc.)
│   │   ├── forms/            # Form components (CandidateForm, InterviewForm, etc.)
│   │   ├── layout/           # Layout components (AppHeader, AppSidebar, etc.)
│   │   └── lists/            # List components (CandidateList, InterviewList, etc.)
│   ├── views/                # Page-level components
│   │   ├── HomeView.vue      # Dashboard/home page
│   │   ├── CandidatesView.vue # Candidate management
│   │   ├── InterviewsView.vue # Interview management
│   │   ├── InterviewExecutionView.vue # Live interview interface
│   │   ├── LoginView.vue     # Authentication
│   │   └── SettingsView.vue  # System settings
│   ├── router/               # Vue Router configuration
│   │   └── index.js          # Route definitions
│   ├── store/                # Pinia state management
│   │   ├── auth.js           # Authentication state
│   │   ├── candidates.js     # Candidate state
│   │   ├── interviews.js     # Interview state
│   │   └── lookup.js         # Lookup data state
│   ├── utils/                # Utility functions
│   │   ├── api.js            # API client configuration
│   │   └── validation.js     # Form validation utilities
│   ├── composables/          # Vue composables (reusable logic)
│   ├── App.vue               # Root Vue component
│   └── main.js               # Vue application entry point
├── public/                   # Static assets
├── index.html                # HTML template
├── package.json              # Node.js dependencies and scripts
├── vite.config.js           # Vite build configuration
├── tailwind.config.js       # Tailwind CSS configuration
└── postcss.config.js        # PostCSS configuration
```

## 🔐 User Roles & Permissions

### 1. System Administrator
- **Full Access**: Complete system administration
- **User Management**: Create, update, deactivate users
- **System Configuration**: Manage lookup tables and settings
- **Audit Access**: View all system activities

### 2. Recruiting Analyst
- **Interview Management**: Create and manage interviews
- **Candidate Access**: View and manage assigned candidates
- **Feedback Review**: Access interview results and feedback
- **Reporting**: Generate recruitment reports

### 3. Candidate (Glober)
- **Interview Access**: Participate in assigned interviews via secure links
- **Limited Access**: No system navigation, direct interview interface only
- **Response Only**: Can only respond to AI interviewer questions

## 🤖 AI Integration

### Interview Flow
1. **Kickoff**: AI receives candidate CV, Job Description, and role context
2. **Conversation**: AI conducts structured technical interview
3. **Assessment**: AI evaluates responses based on technical competencies
4. **Feedback**: System generates structured feedback with 1-5 rankings

### AI Service Configuration
- **Provider**: Globant Enterprise AI (compatible with OpenAI API)
- **Model**: Interviewer_Expert specialized model
- **Timeout**: 60 seconds for responses (with fallback handling)
- **Error Handling**: Graceful degradation with user-friendly messages

### Chat Features
- **Real-time Conversation**: Instant messaging interface
- **Typing Indicators**: Visual feedback during AI processing
- **Message History**: Complete conversation logging
- **Error Recovery**: Automatic retry mechanisms for failed responses

## 📊 Current Project Status

**Phase**: MVP Development (Backend + AI Integration Complete)
**Progress**: ~75% Complete
**Status**: Functional MVP with core features implemented

### ✅ Completed Features
- **Backend API**: Complete FastAPI implementation with all endpoints
- **Database**: SQLite schema with all entities and relationships
- **Authentication**: JWT-based auth with role-based permissions
- **AI Integration**: Working chat system with external AI service
- **File Upload**: CV and Job Description upload functionality
- **User Management**: CRUD operations for all user roles
- **Frontend Foundation**: Vue 3 setup with core components

### 🚧 In Progress
- **Interview Workflow**: Complete interview lifecycle management
- **AI Response Handling**: Improved error handling for slow responses
- **UI Polish**: Enhanced user interface and experience

### 📋 Planned Features
- **Advanced Reporting**: Analytics and recruitment insights
- **Bulk Operations**: Mass candidate and interview management
- **Integration APIs**: Calendar and HR system integrations
- **Mobile Optimization**: Responsive design improvements

## 🧪 Testing

### Backend Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Test AI service specifically
python test_ai.py
```

### Frontend Testing
```bash
# Lint code
npm run lint

# Format code
npm run format

# Build for production
npm run build
```

## 🚀 Deployment

### Production Considerations
- **Database**: Migrate from SQLite to PostgreSQL for scalability
- **File Storage**: Implement cloud storage (AWS S3/Azure Blob)
- **Environment Variables**: Secure secret management
- **Load Balancing**: Multiple backend instances behind load balancer
- **Monitoring**: Application performance monitoring and alerting

### Docker Deployment (Future)
```dockerfile
# Backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend
FROM node:18-alpine
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build
EXPOSE 80
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "80"]
```

## 🤝 Contributing

### Development Guidelines
1. **Code Style**: Follow PEP 8 (backend) and Vue.js style guide (frontend)
2. **Testing**: Write tests for new features and bug fixes
3. **Documentation**: Update README and docstrings for API changes
4. **Commits**: Use conventional commit messages
5. **Memory Bank**: Update memory-bank files for architectural decisions

### Code Quality Tools
- **Backend**: Black (formatting), Flake8 (linting), mypy (type checking)
- **Frontend**: ESLint (linting), Prettier (formatting)

## 📄 License

This project is proprietary software developed for Globant. All rights reserved.

## 📞 Support

For technical support or questions about the system:
- **Backend Issues**: Check FastAPI logs and database connections
- **Frontend Issues**: Check browser console and network requests
- **AI Issues**: Verify AI service configuration and API keys
- **Deployment Issues**: Review environment variables and dependencies

## 🔄 Version History

- **v0.1.0**: Initial MVP with core interview functionality
- **v0.0.1**: Backend foundation and AI integration
- **v0.0.0**: Project initialization and memory bank setup
