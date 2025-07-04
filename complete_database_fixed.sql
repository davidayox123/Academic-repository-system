-- Academic Repository System - Complete Database with Sample Data (Corrected)
-- Drop and recreate database
DROP DATABASE IF EXISTS academic_repo_db;
CREATE DATABASE academic_repo_db;
USE academic_repo_db;

-- 1. DEPARTMENTS TABLE
CREATE TABLE departments (
    department_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    department_name VARCHAR(255) NOT NULL UNIQUE,
    faculty VARCHAR(255) NOT NULL,
    head_of_department VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. USERS TABLE (with all subtypes)
CREATE TABLE users (
    user_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL DEFAULT 'hashed_password',
    role ENUM('STUDENT', 'STAFF', 'SUPERVISOR', 'ADMIN') NOT NULL,
    department_id CHAR(36) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    -- Student attributes
    matric_no VARCHAR(50) UNIQUE,
    level ENUM('100', '200', '300', '400', '500'),
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
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (assigned_department) REFERENCES departments(department_id)
);

-- 3. DOCUMENTS TABLE
CREATE TABLE documents (
    document_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    title VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('SUBMITTED', 'APPROVED', 'REJECTED', 'UNDER_REVIEW') DEFAULT 'SUBMITTED',
    uploader_id CHAR(36) NOT NULL,
    department_id CHAR(36) NOT NULL,
    supervisor_id CHAR(36),
    rejection_reason TEXT,
    file_path VARCHAR(500),
    file_size BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploader_id) REFERENCES users(user_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (supervisor_id) REFERENCES users(user_id),
    UNIQUE KEY unique_title_per_uploader (title, uploader_id)
);

-- 4. METADATA TABLE
CREATE TABLE metadata (
    metadata_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    document_id CHAR(36) NOT NULL UNIQUE,
    keywords TEXT,
    publication_year YEAR,
    authors TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(document_id) ON DELETE CASCADE
);

-- 5. AUDIT_LOG TABLE
CREATE TABLE audit_log (
    log_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    action ENUM('UPLOAD', 'APPROVE', 'REJECT', 'EDIT', 'DELETE', 'DOWNLOAD') NOT NULL,
    document_id CHAR(36),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (document_id) REFERENCES documents(document_id)
);

-- 6. REVIEWS TABLE
CREATE TABLE reviews (
    review_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    document_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comments TEXT,
    decision ENUM('APPROVED', 'REJECTED') NOT NULL,
    FOREIGN KEY (document_id) REFERENCES documents(document_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 7. DOWNLOADS TABLE
CREATE TABLE downloads (
    download_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    document_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    download_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(document_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Insert Departments
INSERT INTO departments (department_id, department_name, faculty, head_of_department) VALUES
('8f9b5b3a-3d1b-4c6a-8a0a-8d7e6f5c4b3a', 'Computer Science', 'Faculty of Science', 'Prof. John Smith'),
(UUID(), 'Physics', 'Faculty of Science', 'Dr. Sarah Johnson'),
(UUID(), 'Mathematics', 'Faculty of Science', 'Prof. Michael Brown'),
(UUID(), 'Environmental Science', 'Faculty of Environmental Studies', 'Dr. Emily Davis'),
(UUID(), 'Chemistry', 'Faculty of Science', 'Prof. David Wilson');

-- Insert Users (Students, Staff, Supervisors, Admins)
SET @cs_dept = (SELECT department_id FROM departments WHERE department_name = 'Computer Science');
SET @physics_dept = (SELECT department_id FROM departments WHERE department_name = 'Physics');
SET @math_dept = (SELECT department_id FROM departments WHERE department_name = 'Mathematics');
SET @env_dept = (SELECT department_id FROM departments WHERE department_name = 'Environmental Science');
SET @chem_dept = (SELECT department_id FROM departments WHERE department_name = 'Chemistry');

-- Students
INSERT INTO users (user_id, first_name, middle_name, last_name, email, role, department_id, matric_no, level, created_at, updated_at) VALUES
('a1b2c3d4-e5f6-7890-1234-567890abcdef', 'John', 'Michael', 'Doe', 'john.doe@student.edu', 'STUDENT', @cs_dept, 'CS/19/001', '400', NOW(), NOW()),
(UUID(), 'Alice', 'Jane', 'Smith', 'alice.smith@student.edu', 'STUDENT', @physics_dept, 'PHY/20/015', '300', NOW(), NOW()),
(UUID(), 'Bob', 'James', 'Johnson', 'bob.johnson@student.edu', 'STUDENT', @math_dept, 'MTH/18/032', '500', NOW(), NOW()),
(UUID(), 'Mary', 'Elizabeth', 'Williams', 'mary.williams@student.edu', 'STUDENT', @env_dept, 'ENV/21/008', '200', NOW(), NOW()),
(UUID(), 'David', 'Paul', 'Brown', 'david.brown@student.edu', 'STUDENT', @cs_dept, 'CS/20/045', '300', NOW(), NOW()),
(UUID(), 'Sarah', 'Michelle', 'Davis', 'sarah.davis@student.edu', 'STUDENT', @chem_dept, 'CHM/19/022', '400', NOW(), NOW()),
(UUID(), 'James', 'Robert', 'Wilson', 'james.wilson@student.edu', 'STUDENT', @physics_dept, 'PHY/21/011', '200', NOW(), NOW()),
(UUID(), 'Lisa', 'Anne', 'Taylor', 'lisa.taylor@student.edu', 'STUDENT', @math_dept, 'MTH/20/028', '300', NOW(), NOW());

-- Staff
INSERT INTO users (user_id, first_name, middle_name, last_name, email, role, department_id, staff_id, position, office_no, created_at, updated_at) VALUES
('b2c3d4e5-f6a7-8901-2345-67890abcdef0', 'Jennifer', 'Marie', 'Anderson', 'jennifer.anderson@staff.edu', 'STAFF', @cs_dept, 'ST001', 'Research Assistant', 'CS-101', NOW(), NOW()),
(UUID(), 'Michael', 'Anthony', 'Thompson', 'michael.thompson@staff.edu', 'STAFF', @physics_dept, 'ST002', 'Lab Technician', 'PHY-205', NOW(), NOW()),
(UUID(), 'Laura', 'Grace', 'Martinez', 'laura.martinez@staff.edu', 'STAFF', @env_dept, 'ST003', 'Administrative Officer', 'ENV-102', NOW(), NOW()),
(UUID(), 'Kevin', 'Christopher', 'Garcia', 'kevin.garcia@staff.edu', 'STAFF', @math_dept, 'ST004', 'Teaching Assistant', 'MTH-301', NOW(), NOW());

-- Supervisors
INSERT INTO users (user_id, first_name, middle_name, last_name, email, role, department_id, assigned_department, specialization_area, max_documents, created_at, updated_at) VALUES
('c3d4e5f6-a7b8-9012-3456-7890abcdef01', 'Dr. Rachel', 'Lynn', 'White', 'rachel.white@supervisor.edu', 'SUPERVISOR', @cs_dept, @cs_dept, 'Artificial Intelligence, Machine Learning', 30, NOW(), NOW()),
(UUID(), 'Prof. Mark', 'Steven', 'Clark', 'mark.clark@supervisor.edu', 'SUPERVISOR', @physics_dept, @physics_dept, 'Quantum Physics, Nuclear Research', 25, NOW(), NOW()),
(UUID(), 'Dr. Amanda', 'Rose', 'Lewis', 'amanda.lewis@supervisor.edu', 'SUPERVISOR', @env_dept, @env_dept, 'Climate Change, Environmental Policy', 35, NOW(), NOW()),
(UUID(), 'Prof. Richard', 'Thomas', 'Hall', 'richard.hall@supervisor.edu', 'SUPERVISOR', @math_dept, @math_dept, 'Pure Mathematics, Statistical Analysis', 20, NOW(), NOW());

-- Admins
INSERT INTO users (user_id, first_name, middle_name, last_name, email, role, department_id, admin_id, admin_level, permissions_scope, created_at, updated_at) VALUES
('d4e5f6a7-b8c9-0123-4567-890abcdef012', 'Super', 'System', 'Administrator', 'super.admin@admin.edu', 'ADMIN', @cs_dept, 'ADM001', 'super', 'Full system access, user management, system configuration', NOW(), NOW()),
(UUID(), 'Department', 'CS', 'Admin', 'cs.admin@admin.edu', 'ADMIN', @cs_dept, 'ADM002', 'department', 'Computer Science department management', NOW(), NOW()),
(UUID(), 'Limited', 'Support', 'Admin', 'support.admin@admin.edu', 'ADMIN', @physics_dept, 'ADM003', 'limited', 'Document review and user support', NOW(), NOW());

-- Insert Documents
SET @student1 = (SELECT user_id FROM users WHERE email = 'john.doe@student.edu');
SET @student2 = (SELECT user_id FROM users WHERE email = 'alice.smith@student.edu');
SET @student3 = (SELECT user_id FROM users WHERE email = 'bob.johnson@student.edu');
SET @supervisor1 = (SELECT user_id FROM users WHERE email = 'rachel.white@supervisor.edu');
SET @supervisor2 = (SELECT user_id FROM users WHERE email = 'mark.clark@supervisor.edu');

INSERT INTO documents (document_id, title, uploader_id, department_id, supervisor_id, status, file_path, file_size, created_at) VALUES
(UUID(), 'Machine Learning Algorithms in Data Mining', @student1, @cs_dept, @supervisor1, 'APPROVED', '/uploads/ml_algorithms.pdf', 2048576, NOW()),
(UUID(), 'Quantum Computing Research Paper', @student2, @physics_dept, @supervisor2, 'UNDER_REVIEW', '/uploads/quantum_computing.pdf', 3145728, NOW()),
(UUID(), 'Statistical Analysis of Population Growth', @student3, @math_dept, NULL, 'SUBMITTED', '/uploads/population_stats.pdf', 1572864, NOW()),
(UUID(), 'AI Ethics in Modern Society', @student1, @cs_dept, @supervisor1, 'APPROVED', '/uploads/ai_ethics.pdf', 1048576, NOW()),
(UUID(), 'Environmental Impact Assessment', (SELECT user_id FROM users WHERE email = 'mary.williams@student.edu'), @env_dept, (SELECT user_id FROM users WHERE email = 'amanda.lewis@supervisor.edu'), 'REJECTED', '/uploads/env_impact.pdf', 2621440, NOW());

-- Insert Metadata
INSERT INTO metadata (metadata_id, document_id, keywords, publication_year, authors) VALUES
(UUID(), (SELECT document_id FROM documents WHERE title = 'Machine Learning Algorithms in Data Mining'), 'machine learning, data mining, algorithms, artificial intelligence', 2024, 'John Michael Doe'),
(UUID(), (SELECT document_id FROM documents WHERE title = 'Quantum Computing Research Paper'), 'quantum computing, quantum physics, research, technology', 2024, 'Alice Jane Smith'),
(UUID(), (SELECT document_id FROM documents WHERE title = 'Statistical Analysis of Population Growth'), 'statistics, population, growth, mathematics, analysis', 2024, 'Bob James Johnson'),
(UUID(), (SELECT document_id FROM documents WHERE title = 'AI Ethics in Modern Society'), 'artificial intelligence, ethics, society, technology, philosophy', 2024, 'John Michael Doe'),
(UUID(), (SELECT document_id FROM documents WHERE title = 'Environmental Impact Assessment'), 'environment, impact assessment, sustainability, ecology', 2024, 'Mary Elizabeth Williams');

-- Insert Reviews
INSERT INTO reviews (review_id, document_id, user_id, comments, decision) VALUES
(UUID(), (SELECT document_id FROM documents WHERE title = 'Machine Learning Algorithms in Data Mining'), @supervisor1, 'Excellent research work with comprehensive analysis and clear methodology.', 'APPROVED'),
(UUID(), (SELECT document_id FROM documents WHERE title = 'AI Ethics in Modern Society'), @supervisor1, 'Well-structured paper addressing important ethical considerations.', 'APPROVED'),
(UUID(), (SELECT document_id FROM documents WHERE title = 'Environmental Impact Assessment'), (SELECT user_id FROM users WHERE email = 'amanda.lewis@supervisor.edu'), 'Insufficient data analysis and weak methodology. Please revise and resubmit.', 'REJECTED');

-- Insert Audit Logs
INSERT INTO audit_log (log_id, user_id, action, document_id, details) VALUES
(UUID(), @student1, 'UPLOAD', (SELECT document_id FROM documents WHERE title = 'Machine Learning Algorithms in Data Mining'), 'Document uploaded successfully'),
(UUID(), @supervisor1, 'APPROVE', (SELECT document_id FROM documents WHERE title = 'Machine Learning Algorithms in Data Mining'), 'Document approved after review'),
(UUID(), @student2, 'UPLOAD', (SELECT document_id FROM documents WHERE title = 'Quantum Computing Research Paper'), 'Document uploaded for review'),
(UUID(), @student1, 'UPLOAD', (SELECT document_id FROM documents WHERE title = 'AI Ethics in Modern Society'), 'Second document uploaded'),
(UUID(), (SELECT user_id FROM users WHERE email = 'mary.williams@student.edu'), 'UPLOAD', (SELECT document_id FROM documents WHERE title = 'Environmental Impact Assessment'), 'Document uploaded for review'),
(UUID(), (SELECT user_id FROM users WHERE email = 'amanda.lewis@supervisor.edu'), 'REJECT', (SELECT document_id FROM documents WHERE title = 'Environmental Impact Assessment'), 'Document rejected - requires revision');

-- Insert Downloads
INSERT INTO downloads (download_id, document_id, user_id) VALUES
(UUID(), (SELECT document_id FROM documents WHERE title = 'Machine Learning Algorithms in Data Mining'), @student2),
(UUID(), (SELECT document_id FROM documents WHERE title = 'Machine Learning Algorithms in Data Mining'), @student3),
(UUID(), (SELECT document_id FROM documents WHERE title = 'AI Ethics in Modern Society'), @student2),
(UUID(), (SELECT document_id FROM documents WHERE title = 'AI Ethics in Modern Society'), (SELECT user_id FROM users WHERE email = 'mary.williams@student.edu'));

-- Display all tables and sample data
SHOW TABLES;

SELECT 'DEPARTMENTS' as 'TABLE';
SELECT department_name, faculty, head_of_department FROM departments;

SELECT 'USERS BY ROLE' as 'TABLE';
SELECT CONCAT(first_name, ' ', last_name) as full_name, email, role, 
       CASE 
         WHEN role = 'STUDENT' THEN matric_no
         WHEN role = 'STAFF' THEN staff_id  
         WHEN role = 'SUPERVISOR' THEN specialization_area
         WHEN role = 'ADMIN' THEN admin_level
       END as role_specific_info
FROM users ORDER BY role;

SELECT 'DOCUMENTS' as 'TABLE';
SELECT d.title, d.status, CONCAT(u.first_name, ' ', u.last_name) as uploader, dept.department_name
FROM documents d 
JOIN users u ON d.uploader_id = u.user_id
JOIN departments dept ON d.department_id = dept.department_id;

SELECT 'METADATA' as 'TABLE';
SELECT d.title, m.keywords, m.publication_year, m.authors
FROM metadata m
JOIN documents d ON m.document_id = d.document_id;

SELECT 'STATISTICS' as 'TABLE';
SELECT 
  (SELECT COUNT(*) FROM users WHERE role = 'STUDENT') as total_students,
  (SELECT COUNT(*) FROM users WHERE role = 'STAFF') as total_staff,
  (SELECT COUNT(*) FROM users WHERE role = 'SUPERVISOR') as total_supervisors,
  (SELECT COUNT(*) FROM users WHERE role = 'ADMIN') as total_admins,
  (SELECT COUNT(*) FROM documents) as total_documents,
  (SELECT COUNT(*) FROM departments) as total_departments;

