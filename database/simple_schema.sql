-- =========================================
-- Academic Research Repository System  
-- Simplified Schema for Presentation
-- =========================================

DROP DATABASE IF EXISTS academic_repo_db;
CREATE DATABASE academic_repo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE academic_repo_db;

-- Departments Table
CREATE TABLE departments (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    faculty VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Users Table (with all user types)
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM('student', 'staff', 'supervisor', 'admin') NOT NULL DEFAULT 'student',
    department_id VARCHAR(36) NOT NULL,
    avatar VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Student fields
    matric_no VARCHAR(20),
    level INT,
    
    -- Staff fields  
    staff_id VARCHAR(20),
    position VARCHAR(100),
    office_no VARCHAR(20),
    
    -- Supervisor fields
    assigned_department VARCHAR(36),
    specialization_area TEXT,
    max_documents INT DEFAULT 50,
    
    -- Admin fields
    admin_id VARCHAR(20),
    admin_level ENUM('super', 'department', 'basic') DEFAULT 'basic',
    permissions_scope JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (department_id) REFERENCES departments(id),
    INDEX idx_email (email),
    INDEX idx_role (role)
);

-- Documents Table  
CREATE TABLE documents (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_name VARCHAR(255) NOT NULL,
    file_size INT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    status ENUM('draft', 'submitted', 'under_review', 'approved', 'rejected', 'published') DEFAULT 'draft',
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
    
    FOREIGN KEY (uploader_id) REFERENCES users(id),
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (supervisor_id) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    
    UNIQUE KEY unique_title_per_uploader (title, uploader_id),
    INDEX idx_status (status),
    INDEX idx_uploader (uploader_id)
);

-- Document Metadata Table
CREATE TABLE document_metadata (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36) NOT NULL UNIQUE,
    keywords TEXT,
    publication_year INT NOT NULL,
    authors JSON NOT NULL,
    abstract TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Reviews Table
CREATE TABLE reviews (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36) NOT NULL,
    reviewer_id VARCHAR(36) NOT NULL,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comments TEXT,
    decision ENUM('approved', 'rejected', 'pending') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(id),
    
    UNIQUE KEY unique_review_per_document_reviewer (document_id, reviewer_id)
);

-- Audit Logs Table
CREATE TABLE audit_logs (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    action ENUM('upload', 'approve', 'reject', 'edit', 'delete', 'download', 'view') NOT NULL,
    document_id VARCHAR(36),
    details JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE SET NULL,
    
    INDEX idx_action (action),
    INDEX idx_timestamp (timestamp)
);

-- Downloads Table
CREATE TABLE downloads (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    download_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Document Collaborators Table
CREATE TABLE document_collaborators (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    role VARCHAR(50) DEFAULT 'collaborator',
    approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_collaborator_per_document (document_id, user_id)
);

-- Create useful views
CREATE VIEW document_full_info AS
SELECT 
    d.id, d.title, d.status, d.upload_date,
    u.name as uploader_name, u.role as uploader_role,
    dept.name as department_name,
    dm.keywords, dm.publication_year, dm.authors
FROM documents d
JOIN users u ON d.uploader_id = u.id
JOIN departments dept ON d.department_id = dept.id
LEFT JOIN document_metadata dm ON d.id = dm.document_id;
