# System Requirements

## Functional Requirements (FR)

### FR-001: User Management
- **FR-001.1:** System must support three user roles: System Administrator, Recruiting Analyst, and Candidate
- **FR-001.2:** System must implement role-based access control following least privilege principle
- **FR-001.3:** System must provide user authentication and authorization mechanisms
- **FR-001.4:** System must allow administrators to create, read, update, and delete user accounts

### FR-002: Candidate Management
- **FR-002.1:** System must store candidate information: First Name, Last Name, Email, ID Document
- **FR-002.2:** System must provide CRUD operations for candidate entities
- **FR-002.3:** System must allow filtering candidates by role and searching by name
- **FR-002.4:** System must validate candidate data integrity and uniqueness

### FR-003: Recruiting Analyst Management
- **FR-003.1:** System must store analyst information: First Name, Last Name, Email
- **FR-003.2:** System must provide CRUD operations for analyst entities
- **FR-003.3:** System must associate analysts with interviews they create

### FR-004: Lookup Table Management
- **FR-004.1:** System must implement a generic lookup table structure with Domain ID, Item ID, and Text fields
- **FR-004.2:** System must support lookup domains for: Roles, Clients, Seniorities, Interview Status
- **FR-004.3:** System must provide CRUD operations for lookup table entries
- **FR-004.4:** System must ensure lookup data consistency across the application

### FR-005: Interview Configuration
- **FR-005.1:** System must allow creating interviews with: Analyst, Candidate, Role, Seniority, CV file, Job Description file, Guidelines, Scheduled DateTime, Status
- **FR-005.2:** System must generate unique, time-sensitive interview links
- **FR-005.3:** System must validate interview link access within ±5 minutes of scheduled time
- **FR-005.4:** System must provide CRUD operations for interview entities
- **FR-005.5:** System must support file upload for CVs and Job Descriptions

### FR-006: Interview Execution
- **FR-006.1:** AI agent must introduce itself and explain the interview process
- **FR-006.2:** AI agent must conduct technical interviews based on Job Description and CV
- **FR-006.3:** AI agent must focus exclusively on quantifiable technical attributes
- **FR-006.4:** AI agent must conclude interviews professionally without revealing results
- **FR-006.5:** System must record complete interview transcripts in the database

### FR-007: Feedback Generation
- **FR-007.1:** System must generate structured feedback with general comments
- **FR-007.2:** System must provide overall ranking from 1-5 scale
- **FR-007.3:** System must evaluate individual skills with 1-5 rankings where:
  - 1 = Cannot perform
  - 2 = Can perform with supervision
  - 3 = Can perform with limited supervision
  - 4 = Can perform with no supervision
  - 5 = Can teach others
- **FR-007.4:** System must store all feedback data in the database

### FR-008: Interview and Candidate Listings
- **FR-008.1:** System must provide filterable interview lists by role and client
- **FR-008.2:** System must provide filterable candidate lists by role and name search
- **FR-008.3:** System must display interview status and feedback when available

## Non-Functional Requirements (NFR)

### NFR-001: Performance
- **NFR-001.1:** System must support concurrent interviews without performance degradation
- **NFR-001.2:** Interview link validation must respond within 2 seconds
- **NFR-001.3:** File uploads must support files up to 10MB in size
- **NFR-001.4:** Database queries must execute within 5 seconds for standard operations

### NFR-002: Security
- **NFR-002.1:** System must implement secure authentication mechanisms
- **NFR-002.2:** System must protect sensitive candidate and interview data
- **NFR-002.3:** System must validate all user inputs to prevent injection attacks
- **NFR-002.4:** System must implement proper session management
- **NFR-002.5:** Interview links must be cryptographically secure and non-guessable

### NFR-003: Usability
- **NFR-003.1:** User interfaces must be intuitive and require minimal training
- **NFR-003.2:** System must provide clear error messages and validation feedback
- **NFR-003.3:** Interview process must be accessible to candidates with basic technical skills
- **NFR-003.4:** System must be responsive and work on desktop and tablet devices

### NFR-004: Reliability
- **NFR-004.1:** System must maintain 99% uptime during business hours
- **NFR-004.2:** System must handle AI service failures gracefully
- **NFR-004.3:** System must implement proper error handling and logging
- **NFR-004.4:** Data integrity must be maintained through proper validation and constraints

### NFR-005: Scalability
- **NFR-005.1:** System architecture must support future feature additions
- **NFR-005.2:** Database design must accommodate growing data volumes
- **NFR-005.3:** API design must support potential mobile applications
- **NFR-005.4:** System must handle increased user load without architectural changes

## Business Rules

### BR-001: Interview Scheduling
- **BR-001.1:** Interview links are only active within ±5 minutes of scheduled time
- **BR-001.2:** Only one active interview per candidate at any given time
- **BR-001.3:** Interviews must be scheduled at least 1 hour in advance

### BR-002: Assessment Scope
- **BR-002.1:** AI evaluation must focus exclusively on quantifiable technical attributes
- **BR-002.2:** Behavioral and subjective criteria are explicitly excluded from assessment
- **BR-002.3:** Skills evaluation must align with Job Description requirements

### BR-003: Data Management
- **BR-003.1:** All interview data must be retained for audit purposes
- **BR-003.2:** Candidate personal information must be handled according to privacy regulations
- **BR-003.3:** File uploads must be validated for type and content safety

### BR-004: User Access
- **BR-004.1:** Candidates can only access their own interview links
- **BR-004.2:** Recruiting Analysts can only manage interviews they created
- **BR-004.3:** System Administrators have full system access

## Edge Cases

### EC-001: Interview Link Access
- **EC-001.1:** Handle attempts to access expired interview links
- **EC-001.2:** Manage multiple simultaneous access attempts to same interview link
- **EC-001.3:** Handle network interruptions during interview sessions

### EC-002: AI Service Integration
- **EC-002.1:** Handle AI service unavailability during scheduled interviews
- **EC-002.2:** Manage incomplete or malformed AI responses
- **EC-002.3:** Handle AI service timeout scenarios

### EC-003: File Upload Management
- **EC-003.1:** Handle corrupted or unreadable uploaded files
- **EC-003.2:** Manage storage capacity limitations
- **EC-003.3:** Handle unsupported file formats gracefully

### EC-004: Data Consistency
- **EC-004.1:** Handle concurrent modifications to interview data
- **EC-004.2:** Manage orphaned records when entities are deleted
- **EC-004.3:** Handle lookup table modifications affecting existing interviews

## Constraints

### Technical Constraints
- **TC-001:** Must use SQLite database for data storage
- **TC-002:** Backend must be implemented using FastAPI framework
- **TC-003:** Frontend must use Vue 3 with Composition API
- **TC-004:** Must integrate with external AI service for interview conduct

### Business Constraints
- **BC-001:** Assessment limited to technical competencies only
- **BC-002:** MVP scope excludes advanced reporting and analytics
- **BC-003:** No integration with external calendar or HR systems
- **BC-004:** English language only for all system interfaces and content
