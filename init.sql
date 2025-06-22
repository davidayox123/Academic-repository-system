-- Academic Repository System Database Schema
-- Create and use the database
CREATE DATABASE IF NOT EXISTS academic_repository;
USE academic_repository;

-- Drop tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS downloads;
DROP TABLE IF EXISTS activity_logs;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS departments;

-- Create departments table
CREATE TABLE departments (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(255) NOT NULL UNIQUE,
    faculty VARCHAR(255) NOT NULL,
    description TEXT,
    head_of_department VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create users table with all subtype attributes
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL DEFAULT 'no_auth',
    role ENUM('student', 'staff', 'supervisor', 'admin') NOT NULL DEFAULT 'student',
    department_id CHAR(36) NOT NULL,
    avatar VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    -- Student attributes
    matric_no VARCHAR(50) UNIQUE,
    level ENUM('100', '200', '300', '400', '500') NULL,
    -- Staff attributes  
    staff_id VARCHAR(50) UNIQUE,
    position VARCHAR(100),
    office_no VARCHAR(20),
    -- Supervisor attributes
    assigned_department CHAR(36),
    specialization_area TEXT,
    max_documents INT DEFAULT 50,
    -- Admin attributes
    admin_id VARCHAR(50) UNIQUE,
    admin_level ENUM('super', 'department', 'limited') DEFAULT 'limited',
    permissions_scope TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email (email),
    INDEX idx_users_role (role),
    INDEX idx_users_department (department_id),
    INDEX idx_users_active (is_active),
    INDEX idx_users_matric (matric_no),
    INDEX idx_users_staff (staff_id),
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT,
    FOREIGN KEY (assigned_department) REFERENCES departments(id) ON DELETE SET NULL
);

-- Create documents table with rejection_reason
CREATE TABLE documents (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL DEFAULT 0,
    mime_type VARCHAR(100),
    category ENUM('research', 'thesis', 'assignment', 'presentation', 'paper', 'report', 'project', 'other') DEFAULT 'other',
    status ENUM('submitted', 'under_review', 'approved', 'rejected') DEFAULT 'submitted',
    uploader_id CHAR(36) NOT NULL,
    supervisor_id CHAR(36),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    review_date TIMESTAMP NULL,
    rejection_reason TEXT NULL,
    download_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_documents_uploader (uploader_id),
    INDEX idx_documents_supervisor (supervisor_id),
    INDEX idx_documents_category (category),
    INDEX idx_documents_status (status),
    INDEX idx_documents_upload_date (upload_date),
    FOREIGN KEY (uploader_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (supervisor_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY unique_title_per_uploader (title, uploader_id)
);

-- Create metadata table
CREATE TABLE metadata (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    document_id CHAR(36) NOT NULL UNIQUE,
    keywords TEXT,
    publication_year YEAR,
    authors TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_metadata_document (document_id),
    INDEX idx_metadata_year (publication_year),
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);

-- Create reviews table
CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    document_id CHAR(36) NOT NULL,
    reviewer_id CHAR(36) NOT NULL,
    review_type ENUM('approve', 'reject', 'request_changes') NOT NULL,
    comments TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_reviews_document (document_id),
    INDEX idx_reviews_reviewer (reviewer_id),
    INDEX idx_reviews_date (review_date),
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create activity_logs table
CREATE TABLE activity_logs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    action_type ENUM('upload', 'download', 'review', 'login', 'logout', 'update', 'delete') NOT NULL,
    resource_type ENUM('document', 'user', 'system') NOT NULL,
    resource_id CHAR(36),
    details TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_activity_user (user_id),
    INDEX idx_activity_type (action_type),
    INDEX idx_activity_resource (resource_type, resource_id),
    INDEX idx_activity_date (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create downloads table
CREATE TABLE downloads (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    document_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    download_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    INDEX idx_downloads_document (document_id),
    INDEX idx_downloads_user (user_id),
    INDEX idx_downloads_date (download_date),
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert sample departments with faculty
INSERT INTO departments (id, name, faculty, description, head_of_department) VALUES
(UUID(), 'Computer Science', 'Faculty of Physical Sciences', 'Department of Computer Science and Engineering', 'Dr. Smith Johnson'),
(UUID(), 'Physics', 'Faculty of Physical Sciences', 'Department of Physics and Astronomy', 'Prof. Sarah Williams'),
(UUID(), 'Environmental Science', 'Faculty of Life Sciences', 'Department of Environmental Studies', 'Dr. Michael Brown'),
(UUID(), 'Mathematics', 'Faculty of Physical Sciences', 'Department of Mathematics', 'Prof. Emily Davis'),
(UUID(), 'Biology', 'Faculty of Life Sciences', 'Department of Biological Sciences', 'Dr. James Wilson');

-- Insert sample users with all subtype attributes
INSERT INTO users (id, email, first_name, middle_name, last_name, role, department_id, matric_no, level, staff_id, position, office_no, specialization_area, max_documents, admin_id, admin_level, permissions_scope) VALUES
-- Students
(UUID(), 'student1@university.edu', 'John', 'Michael', 'Student', 'student', (SELECT id FROM departments WHERE name = 'Computer Science' LIMIT 1), 'CSC/2021/001', '300', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(UUID(), 'student2@university.edu', 'Alice', 'Jane', 'Thompson', 'student', (SELECT id FROM departments WHERE name = 'Physics' LIMIT 1), 'PHY/2020/045', '400', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(UUID(), 'student3@university.edu', 'Bob', 'David', 'Wilson', 'student', (SELECT id FROM departments WHERE name = 'Mathematics' LIMIT 1), 'MAT/2022/123', '200', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(UUID(), 'student4@university.edu', 'Sarah', 'Elizabeth', 'Davis', 'student', (SELECT id FROM departments WHERE name = 'Environmental Science' LIMIT 1), 'ENV/2021/067', '300', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
-- Staff
(UUID(), 'staff1@university.edu', 'Mark', 'Anthony', 'Johnson', 'staff', (SELECT id FROM departments WHERE name = 'Computer Science' LIMIT 1), NULL, NULL, 'STF/CS/001', 'Senior Lecturer', 'CS-101', NULL, NULL, NULL, NULL, NULL),
(UUID(), 'staff2@university.edu', 'Lisa', 'Marie', 'Brown', 'staff', (SELECT id FROM departments WHERE name = 'Physics' LIMIT 1), NULL, NULL, 'STF/PHY/002', 'Associate Professor', 'PHY-205', NULL, NULL, NULL, NULL, NULL),
-- Supervisors
(UUID(), 'supervisor1@university.edu', 'Dr. Jane', 'Patricia', 'Supervisor', 'supervisor', (SELECT id FROM departments WHERE name = 'Physics' LIMIT 1), NULL, NULL, 'SUP/PHY/001', 'Professor', 'PHY-301', 'Quantum Mechanics, Theoretical Physics', 25, NULL, NULL, NULL),
(UUID(), 'supervisor2@university.edu', 'Prof. Robert', 'William', 'Miller', 'supervisor', (SELECT id FROM departments WHERE name = 'Computer Science' LIMIT 1), NULL, NULL, 'SUP/CS/001', 'Professor', 'CS-401', 'Artificial Intelligence, Machine Learning', 30, NULL, NULL, NULL),
-- Admins
(UUID(), 'admin@university.edu', 'System', '', 'Administrator', 'admin', (SELECT id FROM departments WHERE name = 'Computer Science' LIMIT 1), NULL, NULL, 'ADM/SYS/001', 'System Administrator', 'ADM-001', NULL, NULL, 'ADM001', 'super', 'Full system access'),
(UUID(), 'deptadmin@university.edu', 'Department', '', 'Admin', 'admin', (SELECT id FROM departments WHERE name = 'Physics' LIMIT 1), NULL, NULL, 'ADM/PHY/001', 'Department Administrator', 'PHY-101', NULL, NULL, 'ADM002', 'department', 'Physics department only');

-- Insert sample documents with new status values
INSERT INTO documents (id, title, description, filename, file_path, file_size, mime_type, category, status, uploader_id, rejection_reason) VALUES
(UUID(), 'Machine Learning Research Paper', 'A comprehensive study on deep learning algorithms', 'ml_research.pdf', '/uploads/ml_research.pdf', 2048576, 'application/pdf', 'research', 'approved', (SELECT id FROM users WHERE email = 'student1@university.edu' LIMIT 1), NULL),
(UUID(), 'Quantum Physics Thesis', 'Graduate thesis on quantum entanglement', 'quantum_thesis.pdf', '/uploads/quantum_thesis.pdf', 5242880, 'application/pdf', 'thesis', 'under_review', (SELECT id FROM users WHERE email = 'student2@university.edu' LIMIT 1), NULL),
(UUID(), 'Environmental Impact Study', 'Study on climate change effects', 'env_study.pdf', '/uploads/env_study.pdf', 3145728, 'application/pdf', 'report', 'submitted', (SELECT id FROM users WHERE email = 'student4@university.edu' LIMIT 1), NULL),
(UUID(), 'Software Project Documentation', 'Complete documentation for final year project', 'project_docs.pdf', '/uploads/project_docs.pdf', 1024000, 'application/pdf', 'project', 'approved', (SELECT id FROM users WHERE email = 'student1@university.edu' LIMIT 1), NULL),
(UUID(), 'Mathematical Analysis Paper', 'Research on differential equations', 'math_analysis.pdf', '/uploads/math_analysis.pdf', 1500000, 'application/pdf', 'research', 'rejected', (SELECT id FROM users WHERE email = 'student3@university.edu' LIMIT 1), 'Incomplete methodology section. Please revise and resubmit.');

-- Insert metadata for documents
INSERT INTO metadata (id, document_id, keywords, publication_year, authors) VALUES
(UUID(), (SELECT id FROM documents WHERE title = 'Machine Learning Research Paper' LIMIT 1), 'machine learning, deep learning, neural networks, artificial intelligence', 2024, 'John Michael Student'),
(UUID(), (SELECT id FROM documents WHERE title = 'Quantum Physics Thesis' LIMIT 1), 'quantum mechanics, entanglement, physics, theoretical physics', 2024, 'Alice Jane Thompson'),
(UUID(), (SELECT id FROM documents WHERE title = 'Environmental Impact Study' LIMIT 1), 'environment, climate change, sustainability, ecology', 2024, 'Sarah Elizabeth Davis'),
(UUID(), (SELECT id FROM documents WHERE title = 'Software Project Documentation' LIMIT 1), 'software engineering, project management, documentation', 2024, 'John Michael Student'),
(UUID(), (SELECT id FROM documents WHERE title = 'Mathematical Analysis Paper' LIMIT 1), 'mathematics, differential equations, analysis', 2024, 'Bob David Wilson');

-- Insert sample reviews
INSERT INTO reviews (id, document_id, reviewer_id, review_type, comments) VALUES
(UUID(), (SELECT id FROM documents WHERE title = 'Machine Learning Research Paper' LIMIT 1), (SELECT id FROM users WHERE email = 'supervisor@university.edu' LIMIT 1), 'approve', 'Excellent research work with comprehensive analysis.'),
(UUID(), (SELECT id FROM documents WHERE title = 'Software Project Documentation' LIMIT 1), (SELECT id FROM users WHERE email = 'supervisor@university.edu' LIMIT 1), 'approve', 'Well documented project with clear implementation details.');

-- Insert sample activity logs
INSERT INTO activity_logs (id, user_id, action_type, resource_type, resource_id, details) VALUES
(UUID(), (SELECT id FROM users WHERE email = 'student1@university.edu' LIMIT 1), 'upload', 'document', (SELECT id FROM documents WHERE title = 'Machine Learning Research Paper' LIMIT 1), 'Uploaded research paper'),
(UUID(), (SELECT id FROM users WHERE email = 'supervisor@university.edu' LIMIT 1), 'review', 'document', (SELECT id FROM documents WHERE title = 'Machine Learning Research Paper' LIMIT 1), 'Approved document after review'),
(UUID(), (SELECT id FROM users WHERE email = 'student2@university.edu' LIMIT 1), 'upload', 'document', (SELECT id FROM documents WHERE title = 'Quantum Physics Thesis' LIMIT 1), 'Uploaded thesis document');

-- Insert sample downloads
INSERT INTO downloads (id, document_id, user_id) VALUES
(UUID(), (SELECT id FROM documents WHERE title = 'Machine Learning Research Paper' LIMIT 1), (SELECT id FROM users WHERE email = 'student2@university.edu' LIMIT 1)),
(UUID(), (SELECT id FROM documents WHERE title = 'Software Project Documentation' LIMIT 1), (SELECT id FROM users WHERE email = 'student3@university.edu' LIMIT 1));

-- Show created tables
SHOW TABLES;

-- Display sample data
SELECT 'DEPARTMENTS:' as '';
SELECT name, description, head_of_department FROM departments;

SELECT 'USERS:' as '';
SELECT name, email, role, (SELECT name FROM departments WHERE id = users.department_id) as department FROM users;

SELECT 'DOCUMENTS:' as '';
SELECT title, category, status, (SELECT name FROM users WHERE id = documents.uploader_id) as uploader FROM documents;

SELECT 'STATISTICS:' as '';
SELECT 
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM documents) as total_documents,
    (SELECT COUNT(*) FROM departments) as total_departments,
    (SELECT COUNT(*) FROM reviews) as total_reviews;
