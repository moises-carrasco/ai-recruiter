# Data Rules (SQLite Database Guidelines)

These rules define the database naming conventions, data handling guidelines, and SQLite-specific best practices for this project.  
Cline MUST follow these rules when generating or modifying database-related code.
The database file is located in the root folder under the name interview_system.db

---

## 1. Table Naming Conventions

### 1.1 General Rules
- Use **snake_case** for all table names
- Table names must be **plural nouns** (e.g., `candidates`, `interviews`, `lookup_items`)
- Use descriptive, meaningful names that reflect the entity purpose
- Avoid abbreviations unless they are industry-standard
- Maximum length: 63 characters (SQLite limit)

### 1.2 Specific Patterns
- Main entities: `candidates`, `analysts`, `interviews`
- Junction tables: `[entity1]_[entity2]` (e.g., `interview_feedbacks`)
- Lookup tables: `lookup_[domain]` (e.g., `lookup_roles`, `lookup_seniorities`)
- Audit tables: `[table_name]_audit` (e.g., `interviews_audit`)

---

## 2. Column Naming Conventions

### 2.1 General Rules
- Use **snake_case** for all column names
- Column names must be **singular nouns** or descriptive phrases
- Use clear, unambiguous names that indicate the data purpose
- Avoid reserved SQLite keywords as column names
- Maximum length: 63 characters

### 2.2 Standard Column Patterns
- **Primary Key:** Always `id` (INTEGER PRIMARY KEY)
- **Foreign Keys:** `[referenced_table_singular]_id` (e.g., `candidate_id`, `analyst_id`)
- **Timestamps:** 
  - `created_at` (creation timestamp)
  - `updated_at` (last modification timestamp)
  - `deleted_at` (soft delete timestamp, nullable)
- **Status Fields:** `status` or `[entity]_status` (e.g., `interview_status`)
- **Boolean Fields:** `is_[condition]` or `has_[attribute]` (e.g., `is_active`, `has_feedback`)

### 2.3 Specific Field Types
- **Names:** `first_name`, `last_name`, `full_name`
- **Contact:** `email`, `phone_number`
- **Documents:** `document_id`, `cv_file_path`, `job_description_path`
- **URLs/Links:** `interview_link`, `feedback_url`
- **Descriptions:** `description`, `notes`, `comments`

---

## 3. SQLite-Specific Guidelines

### 3.1 Data Types
- **Text Data:** Use `TEXT` for strings, emails, descriptions
- **Numeric Data:** 
  - `INTEGER` for IDs, counts, years
  - `REAL` for decimal numbers, scores
- **Dates/Times:** Use `TEXT` with ISO8601 format (YYYY-MM-DD HH:MM:SS)
- **Binary Data:** Use `BLOB` for file contents (if storing files in DB)
- **Boolean Data:** Use `INTEGER` with 0/1 values

### 3.2 Constraints and Indexes
- **Primary Keys:** Always `INTEGER PRIMARY KEY AUTOINCREMENT`
- **Foreign Keys:** Enable with `PRAGMA foreign_keys = ON`
- **Unique Constraints:** Name as `unq_[table]_[column(s)]`
- **Indexes:** Name as `idx_[table]_[column(s)]`
- **Check Constraints:** Name as `chk_[table]_[condition]`

### 3.3 SQLite Limitations Awareness
- No native ALTER COLUMN support (requires table recreation)
- Limited ALTER TABLE operations
- Case-insensitive LIKE by default
- No native BOOLEAN type
- No native DATE/TIME types

---

## 4. Relationships and Foreign Keys

### 4.1 Foreign Key Naming
- Always follow pattern: `[referenced_table_singular]_id`
- Examples:
  - `candidate_id` references `candidates(id)`
  - `analyst_id` references `analysts(id)`
  - `interview_id` references `interviews(id)`

### 4.2 Relationship Types
- **One-to-Many:** Standard foreign key in child table
- **Many-to-Many:** Junction table with composite primary key
- **One-to-One:** Foreign key with UNIQUE constraint

### 4.3 Referential Integrity
- Always define foreign key constraints
- Use appropriate ON DELETE and ON UPDATE actions:
  - `CASCADE` for dependent data
  - `RESTRICT` for critical references
  - `SET NULL` for optional references

---

## 5. Lookup Tables and Enums

### 5.1 Generic Lookup Table Structure
- Table name: `lookup_items`
- Columns:
  - `id` (INTEGER PRIMARY KEY)
  - `domain_id` (TEXT) - e.g., 'roles', 'seniorities', 'clients'
  - `item_id` (TEXT) - e.g., '001', '002', '003'
  - `text_value` (TEXT) - Display text
  - `is_active` (INTEGER) - 0/1 for soft delete
  - `sort_order` (INTEGER) - For ordering items
  - `created_at` (TEXT)
  - `updated_at` (TEXT)

### 5.2 Domain-Specific Patterns
- **Roles:** domain_id = 'roles', item_id = '001', text_value = 'Data Engineer'
- **Seniorities:** domain_id = 'seniorities', item_id = 'senior', text_value = 'Senior'
- **Clients:** domain_id = 'clients', item_id = 'wb', text_value = 'Northwind Media'

---

## 6. Sensitive Data Handling

### 6.1 Personal Information
- **Email addresses:** Store as-is but ensure proper access controls
- **Document IDs:** Hash or encrypt if containing sensitive information
- **File paths:** Use relative paths, avoid exposing system structure
- **Interview content:** Consider encryption for stored transcripts

### 6.2 Security Considerations
- Never store passwords in plain text
- Use proper hashing for sensitive identifiers
- Implement field-level encryption for PII when required
- Exclude sensitive fields from logs and error messages

### 6.3 Data Retention
- Implement soft delete with `deleted_at` timestamps
- Define retention policies for interview data
- Consider data anonymization for analytics

---

## 7. Versioning and Migrations

### 7.1 Migration File Naming
- Pattern: `YYYYMMDD_HHMMSS_description.sql`
- Example: `20241129_143000_create_candidates_table.sql`
- Use descriptive names that indicate the change purpose

### 7.2 Migration Best Practices
- Always include rollback scripts
- Test migrations on copy of production data
- Use transactions for atomic changes
- Document breaking changes clearly

### 7.3 Schema Versioning
- Maintain schema version in dedicated table: `schema_versions`
- Track applied migrations with timestamps
- Include migration checksums for integrity verification

---

## 8. Audit and Timestamp Requirements

### 8.1 Mandatory Audit Columns
- **All tables must include these audit columns:**
  - `created_at` (TEXT, NOT NULL) - ISO8601 timestamp when record was created
  - `updated_at` (TEXT, NOT NULL) - ISO8601 timestamp when record was last modified

### 8.2 Soft Delete Support
- **For entities requiring soft delete:**
  - `deleted_at` (TEXT, NULLABLE) - ISO8601 timestamp when record was soft deleted
  - Use WHERE deleted_at IS NULL in queries to exclude deleted records

### 8.3 Audit Trail Best Practices
- Always update `updated_at` and `updated_by` on any record modification
- Never update `created_at` or `created_by` after initial insert
- Implement application-level triggers or service layer logic to maintain audit fields
- Consider audit log tables for critical entities (interviews, candidates)

### 8.4 Timestamp Format Standards
- Use ISO8601 format: YYYY-MM-DD HH:MM:SS
- Store all timestamps in UTC
- Application layer handles timezone conversion for display

---

## 9. Data Validation Rules

### 9.1 Required Field Validation
- Use NOT NULL constraints for mandatory fields
- Implement CHECK constraints for data format validation
- Validate email format at database level when possible

### 9.2 Business Rule Constraints
- Interview dates must be in the future when created
- Status transitions must follow defined workflow
- Scores must be within valid ranges (1-5)

### 9.3 Data Consistency
- Ensure referential integrity through foreign keys
- Use triggers for complex business rule enforcement
- Implement unique constraints for natural keys

---

## 10. Integration with Application Layers

### 10.1 SQLAlchemy Model Alignment
- Database column names must match SQLAlchemy model attributes
- Use consistent naming between database and Python code
- Leverage SQLAlchemy's naming conventions for constraints

### 10.2 API Response Mapping
- Database field names should align with Pydantic schema fields
- Use consistent casing (snake_case in DB, camelCase in API if needed)
- Document any field name transformations clearly

### 10.3 Frontend Integration
- Ensure database field names are meaningful for frontend consumption
- Consider API field aliasing for better frontend developer experience
- Maintain consistency in date/time formats across all layers

---

# End of Data Rules
