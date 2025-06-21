-- =========================================
-- Academic Research Repository System
-- Database Management System Course Project
-- Complete SQL Schema Definition
-- =========================================

-- Create Database
CREATE DATABASE IF NOT EXISTS academic_repo_db 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE academic_repo_db;

-- =========================================
-- 1. DEPARTMENTS TABLE
-- =========================================
CREATE TABLE departments (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    faculty VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_department_name (name),
    INDEX idx_faculty (faculty)
);

-- =========================================
-- 2. USERS TABLE (Base table for all user types)
-- =========================================
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM('student', 'staff', 'supervisor', 'admin') NOT NULL DEFAULT 'student',
    department_id VARCHAR(36) NOT NULL,
    avatar VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- User subtype specific fields
    matric_no VARCHAR(20),           -- For students
    level INT,                       -- For students
    staff_id VARCHAR(20),            -- For staff
    position VARCHAR(100),           -- For staff
    office_no VARCHAR(20),           -- For staff
    assigned_department VARCHAR(36), -- For supervisors
    specialization_area TEXT,        -- For supervisors
    max_documents INT DEFAULT 50,    -- For supervisors
    admin_id VARCHAR(20),            -- For admins
    admin_level ENUM('super', 'department', 'basic') DEFAULT 'basic', -- For admins
    permissions_scope JSON,          -- For admins
    
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT,
    
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_department (department_id),
    INDEX idx_matric_no (matric_no),
    INDEX idx_staff_id (staff_id),
    
    -- Constraints based on business rules
    CONSTRAINT chk_student_fields 
        CHECK ((role = 'student' AND matric_no IS NOT NULL AND level IS NOT NULL) OR role != 'student'),
    CONSTRAINT chk_staff_fields 
        CHECK ((role = 'staff' AND staff_id IS NOT NULL AND position IS NOT NULL) OR role != 'staff'),
    CONSTRAINT chk_supervisor_fields 
        CHECK ((role = 'supervisor' AND specialization_area IS NOT NULL) OR role != 'supervisor'),
    CONSTRAINT chk_admin_fields 
        CHECK ((role = 'admin' AND admin_id IS NOT NULL) OR role != 'admin')
);

-- =========================================
-- 3. DOCUMENTS TABLE
-- =========================================
CREATE TABLE documents (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_name VARCHAR(255) NOT NULL,
    file_size INT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    status ENUM('draft', 'submitted', 'under_review', 'approved', 'rejected', 'published') 
           NOT NULL DEFAULT 'draft',
    uploader_id VARCHAR(36) NOT NULL,
    department_id VARCHAR(36) NOT NULL,
    supervisor_id VARCHAR(36),
    rejection_reason TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP NULL,
    approved_by VARCHAR(36),
    download_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (uploader_id) REFERENCES users(id) ON DELETE RESTRICT,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT,
    FOREIGN KEY (supervisor_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL,
    
    INDEX idx_title (title),
    INDEX idx_status (status),
    INDEX idx_uploader (uploader_id),
    INDEX idx_department (department_id),
    INDEX idx_supervisor (supervisor_id),
    INDEX idx_upload_date (upload_date),
    
    -- Business rule: Each document title must be unique per uploader
    UNIQUE KEY unique_title_per_uploader (title, uploader_id),
    
    -- Business rule: Only students and staff can upload documents
    CONSTRAINT chk_uploader_role 
        CHECK (uploader_id IN (
            SELECT id FROM users WHERE role IN ('student', 'staff')
        )),
    
    -- Business rule: Only supervisors can approve documents
    CONSTRAINT chk_supervisor_role 
        CHECK (supervisor_id IS NULL OR supervisor_id IN (
            SELECT id FROM users WHERE role = 'supervisor'
        ))
);

-- =========================================
-- 4. DOCUMENT_METADATA TABLE
-- =========================================
CREATE TABLE document_metadata (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36) NOT NULL UNIQUE,
    keywords TEXT,
    publication_year INT NOT NULL,
    authors JSON NOT NULL,
    abstract TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    
    INDEX idx_publication_year (publication_year),
    INDEX idx_keywords (keywords(255)),
    
    -- Business rule: Publication year must be valid
    CONSTRAINT chk_publication_year 
        CHECK (publication_year >= 1900 AND publication_year <= YEAR(CURDATE()))
);

-- =========================================
-- 5. REVIEWS TABLE
-- =========================================
CREATE TABLE reviews (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36) NOT NULL,
    reviewer_id VARCHAR(36) NOT NULL,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comments TEXT,
    decision ENUM('approved', 'rejected', 'pending') NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE RESTRICT,
    
    INDEX idx_document (document_id),
    INDEX idx_reviewer (reviewer_id),
    INDEX idx_decision (decision),
    INDEX idx_review_date (review_date),
    
    -- Business rule: Only supervisors can review documents
    CONSTRAINT chk_reviewer_role 
        CHECK (reviewer_id IN (
            SELECT id FROM users WHERE role = 'supervisor'
        )),
    
    -- Business rule: One review per document per reviewer
    UNIQUE KEY unique_review_per_document_reviewer (document_id, reviewer_id)
);

-- =========================================
-- 6. AUDIT_LOGS TABLE
-- =========================================
CREATE TABLE audit_logs (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    action ENUM('upload', 'approve', 'reject', 'edit', 'delete', 'download', 'view') NOT NULL,
    document_id VARCHAR(36),
    details JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE SET NULL,
    
    INDEX idx_user (user_id),
    INDEX idx_action (action),
    INDEX idx_document (document_id),
    INDEX idx_timestamp (timestamp)
);

-- =========================================
-- 7. DOWNLOADS TABLE
-- =========================================
CREATE TABLE downloads (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    download_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT,
    
    INDEX idx_document (document_id),
    INDEX idx_user (user_id),
    INDEX idx_timestamp (download_timestamp)
);

-- =========================================
-- 8. DOCUMENT_COLLABORATORS TABLE
-- =========================================
CREATE TABLE document_collaborators (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    role VARCHAR(50) DEFAULT 'collaborator',
    approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    INDEX idx_document (document_id),
    INDEX idx_user (user_id),
    
    -- Business rule: One role per user per document
    UNIQUE KEY unique_collaborator_per_document (document_id, user_id)
);

-- =========================================
-- TRIGGERS FOR BUSINESS RULES
-- =========================================

-- Trigger: Auto-increment download count when document is downloaded
DELIMITER //
CREATE TRIGGER update_download_count
AFTER INSERT ON downloads
FOR EACH ROW
BEGIN
    UPDATE documents 
    SET download_count = download_count + 1 
    WHERE id = NEW.document_id;
END//
DELIMITER ;

-- Trigger: Auto-log document actions
DELIMITER //
CREATE TRIGGER log_document_upload
AFTER INSERT ON documents
FOR EACH ROW
BEGIN
    INSERT INTO audit_logs (id, user_id, action, document_id, timestamp)
    VALUES (UUID(), NEW.uploader_id, 'upload', NEW.id, NOW());
END//
DELIMITER ;

-- Trigger: Log document status changes
DELIMITER //
CREATE TRIGGER log_document_status_change
AFTER UPDATE ON documents
FOR EACH ROW
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO audit_logs (id, user_id, action, document_id, details, timestamp)
        VALUES (
            UUID(), 
            NEW.approved_by, 
            CASE NEW.status 
                WHEN 'approved' THEN 'approve'
                WHEN 'rejected' THEN 'reject'
                ELSE 'edit'
            END,
            NEW.id,
            JSON_OBJECT('old_status', OLD.status, 'new_status', NEW.status),
            NOW()
        );
    END IF;
END//
DELIMITER ;

-- =========================================
-- VIEWS FOR COMMON QUERIES
-- =========================================

-- View: Complete document information with metadata
CREATE VIEW document_full_info AS
SELECT 
    d.id,
    d.title,
    d.description,
    d.status,
    d.upload_date,
    d.download_count,
    u.name AS uploader_name,
    u.email AS uploader_email,
    dept.name AS department_name,
    dept.faculty,
    sup.name AS supervisor_name,
    dm.keywords,
    dm.publication_year,
    dm.authors,
    dm.abstract
FROM documents d
JOIN users u ON d.uploader_id = u.id
JOIN departments dept ON d.department_id = dept.id
LEFT JOIN users sup ON d.supervisor_id = sup.id
LEFT JOIN document_metadata dm ON d.id = dm.document_id;

-- View: User statistics
CREATE VIEW user_statistics AS
SELECT 
    u.id,
    u.name,
    u.email,
    u.role,
    dept.name AS department_name,
    COUNT(d.id) AS documents_uploaded,
    COUNT(r.id) AS reviews_made,
    COUNT(dl.id) AS downloads_made
FROM users u
JOIN departments dept ON u.department_id = dept.id
LEFT JOIN documents d ON u.id = d.uploader_id
LEFT JOIN reviews r ON u.id = r.reviewer_id
LEFT JOIN downloads dl ON u.id = dl.user_id
GROUP BY u.id, u.name, u.email, u.role, dept.name;

-- View: Department statistics
CREATE VIEW department_statistics AS
SELECT 
    dept.id,
    dept.name,
    dept.faculty,
    COUNT(DISTINCT u.id) AS total_users,
    COUNT(DISTINCT CASE WHEN u.role = 'student' THEN u.id END) AS students,
    COUNT(DISTINCT CASE WHEN u.role = 'staff' THEN u.id END) AS staff,
    COUNT(DISTINCT CASE WHEN u.role = 'supervisor' THEN u.id END) AS supervisors,
    COUNT(DISTINCT d.id) AS total_documents,
    COUNT(DISTINCT CASE WHEN d.status = 'approved' THEN d.id END) AS approved_documents,
    COUNT(DISTINCT CASE WHEN d.status = 'rejected' THEN d.id END) AS rejected_documents
FROM departments dept
LEFT JOIN users u ON dept.id = u.department_id
LEFT JOIN documents d ON dept.id = d.department_id
GROUP BY dept.id, dept.name, dept.faculty;
