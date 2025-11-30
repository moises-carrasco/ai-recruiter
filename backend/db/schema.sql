-- ============================================================================
-- Database Schema DDL Script
-- AI Challenge 2025 - Quipu AI Interview System
-- 
-- This script contains the complete database schema definition.
-- This is the SOURCE OF TRUTH for the database structure.
-- 
-- SQLite Database Schema
-- Created: 2024-11-30
-- Version: 1.0.0
-- ============================================================================

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- ============================================================================
-- Schema Version Tracking
-- ============================================================================

CREATE TABLE IF NOT EXISTS schema_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    applied_at TEXT NOT NULL,
    checksum TEXT
);

-- Insert initial version
INSERT OR IGNORE INTO schema_versions (version, description, applied_at, checksum) 
VALUES ('1.0.0', 'Initial schema creation', datetime('now'), 'initial');

-- ============================================================================
-- Core Tables
-- ============================================================================

-- Users Table
-- Purpose: Store system users (Administrators and Recruiting Analysts)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'analyst')),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Users Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(is_active);

-- Candidates Table
-- Purpose: Store candidate information for interviews
CREATE TABLE candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    id_document TEXT NOT NULL UNIQUE,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Candidates Indexes
CREATE INDEX idx_candidates_email ON candidates(email);
CREATE INDEX idx_candidates_id_document ON candidates(id_document);
CREATE INDEX idx_candidates_active ON candidates(is_active);

-- Lookup Items Table
-- Purpose: Generic lookup table for roles, clients, seniorities, and statuses
CREATE TABLE lookup_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    text_value TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    sort_order INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    
    -- Unique constraint for domain + item combination
    CONSTRAINT unq_lookup_domain_item UNIQUE (domain_id, item_id)
);

-- Lookup Items Indexes
CREATE INDEX idx_lookup_domain ON lookup_items(domain_id);
CREATE INDEX idx_lookup_active ON lookup_items(is_active);
CREATE INDEX idx_lookup_sort ON lookup_items(domain_id, sort_order);

-- Interviews Table
-- Purpose: Store interview configurations and scheduling information
CREATE TABLE interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analyst_id INTEGER NOT NULL,
    candidate_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    seniority_id INTEGER NOT NULL,
    client_id INTEGER,
    cv_file_path TEXT,
    job_description_path TEXT,
    interview_guidelines TEXT,
    scheduled_datetime TEXT NOT NULL,
    status_id INTEGER NOT NULL,
    interview_link TEXT UNIQUE,
    link_expires_at TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    
    -- Foreign Key Constraints
    CONSTRAINT fk_interviews_analyst FOREIGN KEY (analyst_id) REFERENCES users(id) ON DELETE RESTRICT,
    CONSTRAINT fk_interviews_candidate FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE RESTRICT,
    CONSTRAINT fk_interviews_role FOREIGN KEY (role_id) REFERENCES lookup_items(id) ON DELETE RESTRICT,
    CONSTRAINT fk_interviews_seniority FOREIGN KEY (seniority_id) REFERENCES lookup_items(id) ON DELETE RESTRICT,
    CONSTRAINT fk_interviews_client FOREIGN KEY (client_id) REFERENCES lookup_items(id) ON DELETE RESTRICT,
    CONSTRAINT fk_interviews_status FOREIGN KEY (status_id) REFERENCES lookup_items(id) ON DELETE RESTRICT
);

-- Interviews Indexes
CREATE INDEX idx_interviews_analyst ON interviews(analyst_id);
CREATE INDEX idx_interviews_candidate ON interviews(candidate_id);
CREATE INDEX idx_interviews_scheduled ON interviews(scheduled_datetime);
CREATE INDEX idx_interviews_status ON interviews(status_id);
CREATE INDEX idx_interviews_link ON interviews(interview_link);
CREATE INDEX idx_interviews_role ON interviews(role_id);
CREATE INDEX idx_interviews_seniority ON interviews(seniority_id);
CREATE INDEX idx_interviews_client ON interviews(client_id);

-- Interview Transcripts Table
-- Purpose: Store complete interview conversation records
CREATE TABLE interview_transcripts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    interview_id INTEGER NOT NULL,
    transcript_content TEXT NOT NULL,
    started_at TEXT,
    completed_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    
    -- Foreign Key Constraints
    CONSTRAINT fk_transcripts_interview FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE
);

-- Interview Transcripts Indexes
CREATE INDEX idx_transcripts_interview ON interview_transcripts(interview_id);

-- Interview Feedbacks Table
-- Purpose: Store AI-generated structured feedback for interviews
CREATE TABLE interview_feedbacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    interview_id INTEGER NOT NULL,
    general_comments TEXT NOT NULL,
    overall_ranking INTEGER NOT NULL CHECK (overall_ranking BETWEEN 1 AND 5),
    skills_evaluation TEXT NOT NULL, -- JSON structure with skill-specific rankings
    strengths TEXT,
    areas_for_improvement TEXT,
    job_fit_assessment TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    
    -- Foreign Key Constraints
    CONSTRAINT fk_feedbacks_interview FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE
);

-- Interview Feedbacks Indexes
CREATE INDEX idx_feedbacks_interview ON interview_feedbacks(interview_id);
CREATE INDEX idx_feedbacks_ranking ON interview_feedbacks(overall_ranking);

-- ============================================================================
-- Initial Data Population
-- ============================================================================

-- Predefined Lookup Items for Roles
INSERT OR IGNORE INTO lookup_items (domain_id, item_id, text_value, sort_order, created_at, updated_at) VALUES
('roles', 'data_engineer', 'Data Engineer', 1, datetime('now'), datetime('now')),
('roles', 'python_developer', 'Python Developer', 2, datetime('now'), datetime('now')),
('roles', 'backend_developer', 'Backend Developer', 3, datetime('now'), datetime('now')),
('roles', 'fullstack_developer', 'Fullstack Developer', 4, datetime('now'), datetime('now')),
('roles', 'devops_engineer', 'DevOps Engineer', 5, datetime('now'), datetime('now')),
('roles', 'ml_engineer', 'Machine Learning Engineer', 6, datetime('now'), datetime('now'));

-- Predefined Lookup Items for Seniorities
INSERT OR IGNORE INTO lookup_items (domain_id, item_id, text_value, sort_order, created_at, updated_at) VALUES
('seniorities', 'junior', 'Junior', 1, datetime('now'), datetime('now')),
('seniorities', 'semi_senior', 'Semi Senior', 2, datetime('now'), datetime('now')),
('seniorities', 'senior', 'Senior', 3, datetime('now'), datetime('now')),
('seniorities', 'lead', 'Lead', 4, datetime('now'), datetime('now')),
('seniorities', 'principal', 'Principal', 5, datetime('now'), datetime('now'));

-- Predefined Lookup Items for Clients
INSERT OR IGNORE INTO lookup_items (domain_id, item_id, text_value, sort_order, created_at, updated_at) VALUES
('clients', 'northwind_media', 'Northwind Media', 1, datetime('now'), datetime('now')),
('clients', 'globex_studios', 'Globex Studios', 2, datetime('now'), datetime('now')),
('clients', 'netflix', 'Netflix', 3, datetime('now'), datetime('now')),
('clients', 'amazon', 'Amazon', 4, datetime('now'), datetime('now')),
('clients', 'microsoft', 'Microsoft', 5, datetime('now'), datetime('now')),
('clients', 'google', 'Google', 6, datetime('now'), datetime('now'));

-- Predefined Lookup Items for Interview Status
INSERT OR IGNORE INTO lookup_items (domain_id, item_id, text_value, sort_order, created_at, updated_at) VALUES
('interview_status', 'registered', 'Registered', 1, datetime('now'), datetime('now')),
('interview_status', 'scheduled', 'Scheduled', 2, datetime('now'), datetime('now')),
('interview_status', 'in_progress', 'In Progress', 3, datetime('now'), datetime('now')),
('interview_status', 'completed', 'Completed', 4, datetime('now'), datetime('now')),
('interview_status', 'cancelled', 'Cancelled', 5, datetime('now'), datetime('now')),
('interview_status', 'no_show', 'No Show', 6, datetime('now'), datetime('now'));

-- ============================================================================
-- Database Constraints and Triggers
-- ============================================================================

-- Trigger to automatically update updated_at timestamp for users
CREATE TRIGGER IF NOT EXISTS trigger_users_updated_at
    AFTER UPDATE ON users
    FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- Trigger to automatically update updated_at timestamp for candidates
CREATE TRIGGER IF NOT EXISTS trigger_candidates_updated_at
    AFTER UPDATE ON candidates
    FOR EACH ROW
BEGIN
    UPDATE candidates SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- Trigger to automatically update updated_at timestamp for lookup_items
CREATE TRIGGER IF NOT EXISTS trigger_lookup_items_updated_at
    AFTER UPDATE ON lookup_items
    FOR EACH ROW
BEGIN
    UPDATE lookup_items SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- Trigger to automatically update updated_at timestamp for interviews
CREATE TRIGGER IF NOT EXISTS trigger_interviews_updated_at
    AFTER UPDATE ON interviews
    FOR EACH ROW
BEGIN
    UPDATE interviews SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- Trigger to automatically update updated_at timestamp for interview_transcripts
CREATE TRIGGER IF NOT EXISTS trigger_transcripts_updated_at
    AFTER UPDATE ON interview_transcripts
    FOR EACH ROW
BEGIN
    UPDATE interview_transcripts SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- Trigger to automatically update updated_at timestamp for interview_feedbacks
CREATE TRIGGER IF NOT EXISTS trigger_feedbacks_updated_at
    AFTER UPDATE ON interview_feedbacks
    FOR EACH ROW
BEGIN
    UPDATE interview_feedbacks SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- ============================================================================
-- Views for Common Queries
-- ============================================================================

-- View for interview details with related information
CREATE VIEW IF NOT EXISTS interview_details AS
SELECT 
    i.id,
    i.scheduled_datetime,
    i.interview_link,
    i.notes,
    u.first_name || ' ' || u.last_name AS analyst_name,
    u.email AS analyst_email,
    c.first_name || ' ' || c.last_name AS candidate_name,
    c.email AS candidate_email,
    c.id_document AS candidate_id_document,
    r.text_value AS role_name,
    s.text_value AS seniority_name,
    cl.text_value AS client_name,
    st.text_value AS status_name,
    i.created_at,
    i.updated_at
FROM interviews i
JOIN users u ON i.analyst_id = u.id
JOIN candidates c ON i.candidate_id = c.id
JOIN lookup_items r ON i.role_id = r.id
JOIN lookup_items s ON i.seniority_id = s.id
LEFT JOIN lookup_items cl ON i.client_id = cl.id
JOIN lookup_items st ON i.status_id = st.id;

-- View for active lookup items by domain
CREATE VIEW IF NOT EXISTS active_lookup_items AS
SELECT 
    id,
    domain_id,
    item_id,
    text_value,
    sort_order
FROM lookup_items 
WHERE is_active = 1
ORDER BY domain_id, sort_order, text_value;

-- ============================================================================
-- Database Statistics and Maintenance
-- ============================================================================

-- Analyze tables for query optimization
ANALYZE;

-- ============================================================================
-- End of Schema
-- ============================================================================

-- Schema creation completed successfully
-- Total tables created: 6 (users, candidates, lookup_items, interviews, interview_transcripts, interview_feedbacks)
-- Total indexes created: 15
-- Total triggers created: 6
-- Total views created: 2
-- Initial data rows inserted: 23 lookup items
