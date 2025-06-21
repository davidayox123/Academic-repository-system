-- Academic Repository System Database Initialization

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS academic_repo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE academic_repo_db;

-- Create user if it doesn't exist
CREATE USER IF NOT EXISTS 'academic_user'@'%' IDENTIFIED BY 'academic_pass';
GRANT ALL PRIVILEGES ON academic_repo_db.* TO 'academic_user'@'%';
FLUSH PRIVILEGES;

-- Insert default departments (as per business requirements)
INSERT IGNORE INTO departments (id, name, faculty, description, created_at) VALUES
('dept-cs', 'Computer Science', 'Engineering', 'Department of Computer Science and Engineering', NOW()),
('dept-math', 'Mathematics', 'Science', 'Department of Mathematics', NOW()),
('dept-physics', 'Physics', 'Science', 'Department of Physics', NOW()),
('dept-chemistry', 'Chemistry', 'Science', 'Department of Chemistry', NOW()),
('dept-biology', 'Biology', 'Science', 'Department of Biology', NOW()),
('dept-business', 'Business Administration', 'Business', 'Department of Business Administration', NOW()),
('dept-psychology', 'Psychology', 'Social Sciences', 'Department of Psychology', NOW()),
('dept-english', 'English Literature', 'Arts', 'Department of English Literature', NOW());

-- Insert default admin user (as per business requirements)
INSERT IGNORE INTO users (id, email, first_name, last_name, hashed_password, role, department_id, admin_id, admin_level, is_active, created_at) VALUES
('admin-1', 'admin@university.edu', 'System', 'Administrator', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'admin', 'dept-cs', 'ADM001', 1, TRUE, NOW());

-- Insert default supervisor (as per business requirements)
INSERT IGNORE INTO users (id, email, first_name, last_name, hashed_password, role, department_id, assigned_department, specialization_area, max_documents, is_active, created_at) VALUES
('supervisor-1', 'supervisor@university.edu', 'Dr. John', 'Smith', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'supervisor', 'dept-cs', 'dept-cs', 'Software Engineering', 100, TRUE, NOW());

-- Insert default staff user
INSERT IGNORE INTO users (id, email, first_name, last_name, hashed_password, role, department_id, staff_id, position, office_no, is_active, created_at) VALUES
('staff-1', 'staff@university.edu', 'Jane', 'Doe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'staff', 'dept-cs', 'STF001', 'Lecturer', 'CS-101', TRUE, NOW());

-- Insert default student user  
INSERT IGNORE INTO users (id, email, first_name, last_name, hashed_password, role, department_id, matric_no, level, is_active, created_at) VALUES
('student-1', 'student@university.edu', 'Alice', 'Johnson', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'student', 'dept-cs', 'CS/19/001', 4, TRUE, NOW());

-- Note: The hashed password above is for 'password123' - change this in production!
