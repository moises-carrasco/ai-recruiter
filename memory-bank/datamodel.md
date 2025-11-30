# Data Model

## Database Source of Truth

**IMPORTANT:** The authoritative source of truth for the database structure is the DDL script located at:
`backend/db/schema.sql`

This script contains:
- Complete table definitions with all columns, constraints, and indexes
- Foreign key relationships and referential integrity rules
- Database triggers for automatic timestamp updates
- Initial data population for lookup tables
- Database views for common queries
- Schema versioning and migration tracking

**This document (datamodel.md) serves as conceptual documentation and reference only.**
For any database structure changes, modifications must be made to the SQL script first, then this documentation should be updated to reflect those changes.

---

## Entity Relationship Overview

The system follows a relational database design with the following core entities and their relationships:

```
Users (1) ----< Interviews (M)
Candidates (1) ----< Interviews (M)
LookupItems (1) ----< Interviews (M) [Role, Seniority, Client, Status]
Interviews (1) ----< InterviewFeedbacks (1)
Interviews (1) ----< InterviewTranscripts (1)
```

## Core Entities

### 1. Users Table
**Purpose:** Store system users (Administrators and Recruiting Analysts)
**Table Name:** `users`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique user identifier |
| first_name | TEXT | NOT NULL | User's first name |
| last_name | TEXT | NOT NULL | User's last name |
| email | TEXT | NOT NULL, UNIQUE | User's email address |
| password_hash | TEXT | NOT NULL | Hashed password |
| role | TEXT | NOT NULL | User role: 'admin' or 'analyst' |
| is_active | INTEGER | NOT NULL DEFAULT 1 | Active status (0/1) |
| created_at | TEXT | NOT NULL | ISO8601 creation timestamp |
| updated_at | TEXT | NOT NULL | ISO8601 last update timestamp |

**Indexes:**
- `idx_users_email` on email
- `idx_users_role` on role

### 2. Candidates Table
**Purpose:** Store candidate information for interviews
**Table Name:** `candidates`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique candidate identifier |
| first_name | TEXT | NOT NULL | Candidate's first name |
| last_name | TEXT | NOT NULL | Candidate's last name |
| email | TEXT | NOT NULL, UNIQUE | Candidate's email address |
| id_document | TEXT | NOT NULL, UNIQUE | Candidate's ID document |
| is_active | INTEGER | NOT NULL DEFAULT 1 | Active status (0/1) |
| created_at | TEXT | NOT NULL | ISO8601 creation timestamp |
| updated_at | TEXT | NOT NULL | ISO8601 last update timestamp |

**Indexes:**
- `idx_candidates_email` on email
- `idx_candidates_id_document` on id_document

### 3. Lookup Items Table
**Purpose:** Generic lookup table for roles, clients, seniorities, and statuses
**Table Name:** `lookup_items`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique lookup item identifier |
| domain_id | TEXT | NOT NULL | Domain identifier (e.g., 'roles', 'clients') |
| item_id | TEXT | NOT NULL | Item identifier within domain |
| text_value | TEXT | NOT NULL | Display text for the item |
| is_active | INTEGER | NOT NULL DEFAULT 1 | Active status (0/1) |
| sort_order | INTEGER | DEFAULT 0 | Ordering for display |
| created_at | TEXT | NOT NULL | ISO8601 creation timestamp |
| updated_at | TEXT | NOT NULL | ISO8601 last update timestamp |

**Unique Constraints:**
- `unq_lookup_domain_item` on (domain_id, item_id)

**Indexes:**
- `idx_lookup_domain` on domain_id
- `idx_lookup_active` on is_active

**Predefined Domains:**
- **roles:** Technical roles (e.g., 'data_engineer', 'python_developer')
- **clients:** Globant clients (e.g., 'northwind_media', 'globex_studios')
- **seniorities:** Experience levels (e.g., 'junior', 'senior', 'lead')
- **interview_status:** Interview states (e.g., 'registered', 'executed', 'not_executed')

### 4. Interviews Table
**Purpose:** Store interview configurations and scheduling information
**Table Name:** `interviews`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique interview identifier |
| analyst_id | INTEGER | NOT NULL, FK to users.id | Recruiting analyst who created the interview |
| candidate_id | INTEGER | NOT NULL, FK to candidates.id | Candidate being interviewed |
| role_id | INTEGER | NOT NULL, FK to lookup_items.id | Role being applied for |
| seniority_id | INTEGER | NOT NULL, FK to lookup_items.id | Expected seniority level |
| client_id | INTEGER | FK to lookup_items.id | Client for the position |
| cv_file_path | TEXT | | Path to uploaded CV file |
| job_description_path | TEXT | | Path to uploaded Job Description file |
| interview_guidelines | TEXT | | Specific guidelines for the interview |
| scheduled_datetime | TEXT | NOT NULL | ISO8601 scheduled date and time |
| status_id | INTEGER | NOT NULL, FK to lookup_items.id | Current interview status |
| interview_link | TEXT | UNIQUE | Unique link for candidate access |
| link_expires_at | TEXT | | ISO8601 expiration time for the link |
| notes | TEXT | | Additional notes about the interview |
| created_at | TEXT | NOT NULL | ISO8601 creation timestamp |
| updated_at | TEXT | NOT NULL | ISO8601 last update timestamp |

**Foreign Key Constraints:**
- `fk_interviews_analyst` FOREIGN KEY (analyst_id) REFERENCES users(id)
- `fk_interviews_candidate` FOREIGN KEY (candidate_id) REFERENCES candidates(id)
- `fk_interviews_role` FOREIGN KEY (role_id) REFERENCES lookup_items(id)
- `fk_interviews_seniority` FOREIGN KEY (seniority_id) REFERENCES lookup_items(id)
- `fk_interviews_client` FOREIGN KEY (client_id) REFERENCES lookup_items(id)
- `fk_interviews_status` FOREIGN KEY (status_id) REFERENCES lookup_items(id)

**Indexes:**
- `idx_interviews_analyst` on analyst_id
- `idx_interviews_candidate` on candidate_id
- `idx_interviews_scheduled` on scheduled_datetime
- `idx_interviews_status` on status_id
- `idx_interviews_link` on interview_link

### 5. Interview Transcripts Table
**Purpose:** Store complete interview conversation records
**Table Name:** `interview_transcripts`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique transcript identifier |
| interview_id | INTEGER | NOT NULL, FK to interviews.id | Associated interview |
| transcript_content | TEXT | NOT NULL | Complete interview conversation |
| started_at | TEXT | | ISO8601 interview start time |
| completed_at | TEXT | | ISO8601 interview completion time |
| created_at | TEXT | NOT NULL | ISO8601 creation timestamp |
| updated_at | TEXT | NOT NULL | ISO8601 last update timestamp |

**Foreign Key Constraints:**
- `fk_transcripts_interview` FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE

**Indexes:**
- `idx_transcripts_interview` on interview_id

### 6. Interview Feedbacks Table
**Purpose:** Store AI-generated structured feedback for interviews
**Table Name:** `interview_feedbacks`

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique feedback identifier |
| interview_id | INTEGER | NOT NULL, FK to interviews.id | Associated interview |
| general_comments | TEXT | NOT NULL | Overall assessment comments |
| overall_ranking | INTEGER | NOT NULL CHECK (overall_ranking BETWEEN 1 AND 5) | General ranking 1-5 |
| skills_evaluation | TEXT | NOT NULL | JSON structure with skill-specific rankings |
| strengths | TEXT | | Identified candidate strengths |
| areas_for_improvement | TEXT | | Areas needing improvement |
| job_fit_assessment | TEXT | | Assessment of candidate-JD alignment |
| created_at | TEXT | NOT NULL | ISO8601 creation timestamp |
| updated_at | TEXT | NOT NULL | ISO8601 last update timestamp |

**Foreign Key Constraints:**
- `fk_feedbacks_interview` FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE

**Indexes:**
- `idx_feedbacks_interview` on interview_id
- `idx_feedbacks_ranking` on overall_ranking

**Skills Evaluation JSON Structure:**
```json
{
  "technical_skills": [
    {
      "skill_name": "Python Programming",
      "ranking": 4,
      "comments": "Strong understanding of Python fundamentals"
    },
    {
      "skill_name": "Database Design",
      "ranking": 3,
      "comments": "Good knowledge but needs more experience with complex schemas"
    }
  ],
  "experience_areas": [
    {
      "area": "Years of Experience",
      "ranking": 3,
      "comments": "5 years experience aligns with senior level requirements"
    }
  ]
}
```

## Data Relationships

### One-to-Many Relationships
1. **Users → Interviews:** One analyst can create multiple interviews
2. **Candidates → Interviews:** One candidate can have multiple interviews (for different roles)
3. **Lookup Items → Interviews:** Each lookup item can be referenced by multiple interviews

### One-to-One Relationships
1. **Interviews → Interview Transcripts:** Each interview has one transcript
2. **Interviews → Interview Feedbacks:** Each interview has one feedback record

## Data Integrity Rules

### Referential Integrity
- All foreign key relationships must be maintained
- Cascade delete for dependent records (transcripts, feedbacks)
- Restrict delete for referenced lookup items

### Business Rules Constraints
1. **Interview Scheduling:** scheduled_datetime must be in the future when created
2. **Link Expiration:** link_expires_at must be within ±5 minutes of scheduled_datetime
3. **Status Transitions:** Interview status must follow valid workflow transitions
4. **Ranking Validation:** All ranking fields must be between 1 and 5
5. **Unique Constraints:** Email addresses and ID documents must be unique

### Data Validation
1. **Email Format:** Valid email format for users and candidates
2. **DateTime Format:** All timestamps in ISO8601 format (YYYY-MM-DD HH:MM:SS)
3. **File Paths:** Valid file paths for uploaded documents
4. **JSON Structure:** Valid JSON format for skills_evaluation field

## Audit Trail

### Mandatory Audit Columns
All tables include:
- `created_at`: Record creation timestamp
- `updated_at`: Last modification timestamp

### Soft Delete Support
Tables with `is_active` column support soft delete:
- `users`
- `candidates`
- `lookup_items`

### Change Tracking
- Application layer maintains audit trail through updated_at timestamps
- Critical operations logged through application logging system

## Performance Considerations

### Indexing Strategy
- Primary keys automatically indexed
- Foreign keys indexed for join performance
- Frequently queried columns indexed (email, status, scheduled_datetime)
- Composite indexes for common filter combinations

### Query Optimization
- Use appropriate WHERE clauses with indexed columns
- Implement pagination for large result sets
- Optimize JOIN operations with proper indexing

## Security Considerations

### Sensitive Data Protection
- Password hashing for user authentication
- Secure file path storage without exposing system structure
- Interview link generation using cryptographically secure methods

### Access Control
- Role-based data access through application layer
- Candidate data access restricted to authorized users
- Interview data access limited to creating analyst and administrators

## Migration Strategy

### Schema Versioning
- Maintain schema version tracking
- Document all schema changes
- Provide rollback scripts for migrations
- Test migrations on data copies before production deployment
