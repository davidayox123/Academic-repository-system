-- Academic Repository System Database Initialization

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS academic_repo_db;
USE academic_repo_db;

-- Create user if it doesn't exist
CREATE USER IF NOT EXISTS 'academic_user'@'%' IDENTIFIED BY 'academic_pass';
GRANT ALL PRIVILEGES ON academic_repo_db.* TO 'academic_user'@'%';
FLUSH PRIVILEGES;

-- Insert default departments
INSERT IGNORE INTO departments (id, name, faculty, description, created_at) VALUES
('dept-1', 'Computer Science', 'Engineering', 'Department of Computer Science and Engineering', NOW()),
('dept-2', 'Mathematics', 'Science', 'Department of Mathematics', NOW()),
('dept-3', 'Physics', 'Science', 'Department of Physics', NOW()),
('dept-4', 'Chemistry', 'Science', 'Department of Chemistry', NOW()),
('dept-5', 'Biology', 'Science', 'Department of Biology', NOW()),
('dept-6', 'Business Administration', 'Business', 'Department of Business Administration', NOW()),
('dept-7', 'Psychology', 'Social Sciences', 'Department of Psychology', NOW()),
('dept-8', 'English Literature', 'Arts', 'Department of English Literature', NOW());

-- Insert default admin user
INSERT IGNORE INTO users (id, name, email, hashed_password, role, department_id, is_active, created_at) VALUES
('admin-1', 'System Administrator', 'admin@university.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'admin', 'dept-1', TRUE, NOW()),
('supervisor-1', 'Dr. John Smith', 'supervisor@university.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'supervisor', 'dept-1', TRUE, NOW()),
('student-1', 'Jane Doe', 'student@university.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'student', 'dept-1', TRUE, NOW());

-- Note: The hashed password above is for 'password123' - change this in production!
