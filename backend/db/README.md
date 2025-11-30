# Database Schema Documentation

## Overview

This directory contains the complete database schema definition for the AI Challenge 2025 - Quipu AI Interview System. The database uses SQLite and follows strict naming conventions and data integrity rules.

## Files

- **`schema.sql`** - The authoritative source of truth for the database structure
- **`test_schema.sql`** - Test script to verify schema functionality
- **`README.md`** - This documentation file

## Database Structure

### Core Tables

1. **`users`** - System users (administrators and recruiting analysts)
2. **`candidates`** - Interview candidates
3. **`lookup_items`** - Generic lookup table for roles, clients, seniorities, and statuses
4. **`interviews`** - Interview configurations and scheduling
5. **`interview_transcripts`** - Complete interview conversation records
6. **`interview_feedbacks`** - AI-generated structured feedback

### Schema Features

- **Foreign Key Constraints**: Enforced referential integrity
- **Check Constraints**: Data validation at database level
- **Unique Constraints**: Prevent duplicate data
- **Indexes**: Optimized for common query patterns
- **Triggers**: Automatic timestamp updates
- **Views**: Pre-built queries for common operations
- **Initial Data**: Pre-populated lookup items

## Usage Instructions

### Creating the Database

To create a new database with the complete schema:

```bash
# Navigate to the db directory
cd backend/db

# Create a new SQLite database
sqlite3 your_database.db < schema.sql
```

### Testing the Schema

To verify the schema works correctly:

```bash
# Run the test script
sqlite3 test_database.db < test_schema.sql

# Clean up test database
rm test_database.db
```

### Schema Verification

The test script will:
- Create all tables with proper constraints
- Populate lookup items with initial data
- Test foreign key relationships
- Verify constraint enforcement
- Test database views
- Validate triggers

## Schema Versioning

The schema includes a `schema_versions` table to track database migrations:

```sql
SELECT * FROM schema_versions;
```

Current version: **1.0.0**

## Data Rules Compliance

This schema follows the project's data rules defined in `.clinerules/data_rules.md`:

### Naming Conventions
- **Tables**: snake_case, plural nouns (e.g., `candidates`, `interviews`)
- **Columns**: snake_case, singular nouns (e.g., `first_name`, `email`)
- **Foreign Keys**: `[table_singular]_id` pattern (e.g., `candidate_id`)
- **Indexes**: `idx_[table]_[column(s)]` pattern
- **Constraints**: `unq_`, `chk_`, `fk_` prefixes

### Data Types
- **Text**: `TEXT` for strings, emails, descriptions
- **Numbers**: `INTEGER` for IDs, counts; `REAL` for decimals
- **Timestamps**: `TEXT` with ISO8601 format
- **Booleans**: `INTEGER` with 0/1 values

### Audit Trail
- All tables include `created_at` and `updated_at` timestamps
- Automatic timestamp updates via triggers
- Soft delete support with `is_active` column where applicable

## Lookup Items Structure

The `lookup_items` table uses a generic structure for all lookup data:

### Domains
- **`roles`**: Technical roles (data_engineer, python_developer, etc.)
- **`seniorities`**: Experience levels (junior, senior, lead, etc.)
- **`clients`**: Globant clients (northwind_media, globex_studios, etc.)
- **`interview_status`**: Interview states (registered, completed, etc.)

### Adding New Lookup Items

```sql
INSERT INTO lookup_items (domain_id, item_id, text_value, sort_order, created_at, updated_at)
VALUES ('domain', 'item_key', 'Display Text', 1, datetime('now'), datetime('now'));
```

## Database Views

### `interview_details`
Complete interview information with related data:
```sql
SELECT * FROM interview_details WHERE status_name = 'Completed';
```

### `active_lookup_items`
All active lookup items organized by domain:
```sql
SELECT * FROM active_lookup_items WHERE domain_id = 'roles';
```

## Performance Considerations

### Indexes
- Primary keys automatically indexed
- Foreign keys indexed for join performance
- Frequently queried columns indexed (email, status, dates)
- Composite indexes for common filter combinations

### Query Optimization
- Use indexed columns in WHERE clauses
- Implement pagination for large result sets
- Leverage views for complex joins

## Security Features

- Password hashing required for user authentication
- Foreign key constraints prevent orphaned records
- Check constraints validate data integrity
- Unique constraints prevent duplicate critical data

## Migration Strategy

When making schema changes:

1. **Update `schema.sql`** - The source of truth
2. **Create migration script** - For existing databases
3. **Update version** - In `schema_versions` table
4. **Test thoroughly** - Use test script
5. **Update documentation** - This README and `datamodel.md`

## Common Operations

### Creating a User
```sql
INSERT INTO users (first_name, last_name, email, password_hash, role, created_at, updated_at)
VALUES ('John', 'Analyst', 'john@example.com', 'hashed_password', 'analyst', datetime('now'), datetime('now'));
```

### Creating an Interview
```sql
INSERT INTO interviews (
    analyst_id, candidate_id, role_id, seniority_id, status_id,
    scheduled_datetime, created_at, updated_at
) VALUES (
    1, 1,
    (SELECT id FROM lookup_items WHERE domain_id = 'roles' AND item_id = 'data_engineer'),
    (SELECT id FROM lookup_items WHERE domain_id = 'seniorities' AND item_id = 'senior'),
    (SELECT id FROM lookup_items WHERE domain_id = 'interview_status' AND item_id = 'registered'),
    datetime('now', '+1 day'),
    datetime('now'),
    datetime('now')
);
```

### Querying Interview Details
```sql
SELECT 
    candidate_name,
    role_name,
    seniority_name,
    scheduled_datetime,
    status_name
FROM interview_details
WHERE analyst_email = 'john@example.com'
ORDER BY scheduled_datetime DESC;
```

## Troubleshooting

### Foreign Key Errors
Ensure foreign key constraints are enabled:
```sql
PRAGMA foreign_keys = ON;
```

### Constraint Violations
Check constraint definitions:
```sql
.schema table_name
```

### Performance Issues
Analyze query performance:
```sql
EXPLAIN QUERY PLAN SELECT ...;
```

## Support

For questions about the database schema:
1. Check this documentation
2. Review the data rules in `.clinerules/data_rules.md`
3. Examine the test script for usage examples
4. Consult the conceptual documentation in `memory-bank/datamodel.md`

---

**Remember**: `backend/db/schema.sql` is the authoritative source of truth for the database structure. All changes must be made there first, then reflected in documentation.
