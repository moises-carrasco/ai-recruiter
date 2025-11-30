-- ============================================================================
-- Schema Test Script
-- AI Challenge 2025 - Quipu AI Interview System
-- 
-- This script tests the database schema by creating a temporary database
-- and running basic operations to verify structure and constraints.
-- ============================================================================

-- Test database creation and basic operations
.echo on

-- Load the main schema
.read schema.sql

-- Verify tables were created
.tables

-- Check schema for each table
.schema users
.schema candidates
.schema lookup_items
.schema interviews
.schema interview_transcripts
.schema interview_feedbacks

-- Test basic insertions to verify constraints work

-- Test user insertion
INSERT INTO users (first_name, last_name, email, password_hash, role, created_at, updated_at)
VALUES ('Test', 'Analyst', 'test@example.com', 'hashed_password', 'analyst', datetime('now'), datetime('now'));

-- Test candidate insertion
INSERT INTO candidates (first_name, last_name, email, id_document, created_at, updated_at)
VALUES ('John', 'Doe', 'john.doe@example.com', 'ID123456', datetime('now'), datetime('now'));

-- Verify lookup items were populated
SELECT COUNT(*) as total_lookup_items FROM lookup_items;
SELECT domain_id, COUNT(*) as count FROM lookup_items GROUP BY domain_id;

-- Test interview insertion with foreign keys
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

-- Test views
SELECT * FROM interview_details;
SELECT * FROM active_lookup_items WHERE domain_id = 'roles';

-- Test constraints (these should fail)
.echo off
.print "Testing constraint violations (should show errors):"
.echo on

-- Try to insert duplicate email (should fail)
INSERT INTO users (first_name, last_name, email, password_hash, role, created_at, updated_at)
VALUES ('Another', 'User', 'test@example.com', 'hashed_password', 'admin', datetime('now'), datetime('now'));

-- Try to insert invalid role (should fail)
INSERT INTO users (first_name, last_name, email, password_hash, role, created_at, updated_at)
VALUES ('Invalid', 'User', 'invalid@example.com', 'hashed_password', 'invalid_role', datetime('now'), datetime('now'));

-- Try to insert invalid ranking (should fail)
INSERT INTO interview_feedbacks (interview_id, general_comments, overall_ranking, skills_evaluation, created_at, updated_at)
VALUES (1, 'Test feedback', 6, '{}', datetime('now'), datetime('now'));

.echo off
.print "Schema test completed successfully!"
