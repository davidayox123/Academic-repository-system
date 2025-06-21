-- =========================================
-- Academic Research Repository System
-- Sample Data for Presentation
-- Database Management System Course Project
-- =========================================

USE academic_repo_db;

-- =========================================
-- 1. INSERT SAMPLE DEPARTMENTS
-- =========================================
INSERT INTO departments (id, name, faculty, description) VALUES
('dept-001', 'Computer Science', 'Engineering', 'Department of Computer Science and Engineering'),
('dept-002', 'Mathematics', 'Science', 'Department of Mathematics'),
('dept-003', 'Physics', 'Science', 'Department of Physics'),
('dept-004', 'Chemistry', 'Science', 'Department of Chemistry'),
('dept-005', 'Business Administration', 'Business', 'Department of Business Administration'),
('dept-006', 'Psychology', 'Social Sciences', 'Department of Psychology'),
('dept-007', 'English Literature', 'Arts', 'Department of English Literature'),
('dept-008', 'Mechanical Engineering', 'Engineering', 'Department of Mechanical Engineering');

-- =========================================
-- 2. INSERT SAMPLE USERS (All Types)
-- =========================================

-- Admins
INSERT INTO users (id, name, email, hashed_password, role, department_id, admin_id, admin_level, permissions_scope, is_active) VALUES
('admin-001', 'Dr. Sarah Johnson', 'admin@university.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'admin', 'dept-001', 'ADM001', 'super', '{"manage_users": true, "manage_departments": true, "view_all_documents": true}', TRUE);

-- Supervisors
INSERT INTO users (id, name, email, hashed_password, role, department_id, assigned_department, specialization_area, max_documents, is_active) VALUES
('sup-001', 'Prof. Michael Chen', 'supervisor1@university.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'supervisor', 'dept-001', 'dept-001', 'Machine Learning and AI', 100, TRUE),
('sup-002', 'Dr. Emily Rodriguez', 'supervisor2@university.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'supervisor', 'dept-002', 'dept-002', 'Applied Mathematics', 75, TRUE),
('sup-003', 'Prof. David Thompson', 'supervisor3@university.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'supervisor', 'dept-003', 'dept-003', 'Quantum Physics', 80, TRUE);

-- Staff Members
INSERT INTO users (id, name, email, hashed_password, role, department_id, staff_id, position, office_no, is_active) VALUES
('staff-001', 'Dr. Lisa Wang', 'staff1@university.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'staff', 'dept-001', 'STF001', 'Senior Lecturer', 'ENG-301', TRUE),
('staff-002', 'Mr. James Wilson', 'staff2@university.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'staff', 'dept-004', 'STF002', 'Research Assistant', 'SCI-205', TRUE),
('staff-003', 'Dr. Maria Santos', 'staff3@university.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'staff', 'dept-005', 'STF003', 'Associate Professor', 'BUS-101', TRUE);

-- Students
INSERT INTO users (id, name, email, hashed_password, role, department_id, matric_no, level, is_active) VALUES
('student-001', 'Alice Johnson', 'alice.johnson@student.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'student', 'dept-001', 'CS/2021/001', 400, TRUE),
('student-002', 'Bob Smith', 'bob.smith@student.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'student', 'dept-001', 'CS/2020/045', 500, TRUE),
('student-003', 'Carol Brown', 'carol.brown@student.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'student', 'dept-002', 'MA/2021/012', 300, TRUE),
('student-004', 'David Lee', 'david.lee@student.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'student', 'dept-003', 'PH/2019/078', 500, TRUE),
('student-005', 'Emma Davis', 'emma.davis@student.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewddE.8qpjGhYf6O', 'student', 'dept-004', 'CH/2020/023', 400, TRUE);

-- =========================================
-- 3. INSERT SAMPLE DOCUMENTS
-- =========================================
INSERT INTO documents (id, title, description, file_name, file_size, file_type, file_path, status, uploader_id, department_id, supervisor_id, upload_date) VALUES
('doc-001', 'Machine Learning Applications in Healthcare', 'A comprehensive study on ML applications in medical diagnosis', 'ml_healthcare_2024.pdf', 2048576, 'pdf', '/uploads/ml_healthcare_2024.pdf', 'approved', 'student-001', 'dept-001', 'sup-001', '2024-01-15 10:30:00'),
('doc-002', 'Advanced Calculus Solutions Manual', 'Complete solutions for advanced calculus problems', 'calculus_solutions.pdf', 1536000, 'pdf', '/uploads/calculus_solutions.pdf', 'under_review', 'student-003', 'dept-002', 'sup-002', '2024-02-20 14:45:00'),
('doc-003', 'Quantum Computing Fundamentals', 'Introduction to quantum computing principles', 'quantum_computing.pdf', 3072000, 'pdf', '/uploads/quantum_computing.pdf', 'submitted', 'staff-001', 'dept-001', 'sup-001', '2024-03-10 09:15:00'),
('doc-004', 'Climate Change Data Analysis', 'Statistical analysis of climate change patterns', 'climate_analysis.pdf', 2560000, 'pdf', '/uploads/climate_analysis.pdf', 'approved', 'student-004', 'dept-003', 'sup-003', '2024-01-25 16:20:00'),
('doc-005', 'Organic Chemistry Lab Manual', 'Laboratory procedures for organic chemistry', 'org_chem_lab.pdf', 1792000, 'pdf', '/uploads/org_chem_lab.pdf', 'rejected', 'student-005', 'dept-004', NULL, '2024-02-05 11:00:00');

-- =========================================
-- 4. INSERT DOCUMENT METADATA
-- =========================================
INSERT INTO document_metadata (id, document_id, keywords, publication_year, authors, abstract) VALUES
('meta-001', 'doc-001', 'machine learning, healthcare, AI, medical diagnosis, neural networks', 2024, '["Alice Johnson", "Prof. Michael Chen"]', 'This research explores the application of machine learning algorithms in healthcare, specifically focusing on medical diagnosis and patient care optimization.'),
('meta-002', 'doc-002', 'calculus, mathematics, solutions, differential equations', 2024, '["Carol Brown"]', 'A comprehensive collection of solved problems in advanced calculus, covering differential equations, integration techniques, and series convergence.'),
('meta-003', 'doc-003', 'quantum computing, quantum mechanics, algorithms, qubits', 2024, '["Dr. Lisa Wang", "Prof. Michael Chen"]', 'An introduction to quantum computing principles, exploring quantum algorithms and their potential applications in solving complex computational problems.'),
('meta-004', 'doc-004', 'climate change, data analysis, statistics, environmental science', 2024, '["David Lee", "Prof. David Thompson"]', 'Statistical analysis of global climate data over the past 50 years, identifying patterns and trends in temperature and precipitation changes.'),
('meta-005', 'doc-005', 'organic chemistry, laboratory, experiments, synthesis', 2024, '["Emma Davis"]', 'A practical guide to organic chemistry laboratory procedures, including synthesis techniques and safety protocols.');

-- =========================================
-- 5. INSERT SAMPLE REVIEWS
-- =========================================
INSERT INTO reviews (id, document_id, reviewer_id, review_date, comments, decision) VALUES
('rev-001', 'doc-001', 'sup-001', '2024-01-20 15:30:00', 'Excellent research work with innovative approaches to ML in healthcare. Approved for publication.', 'approved'),
('rev-002', 'doc-002', 'sup-002', '2024-02-25 10:15:00', 'Good work but needs more detailed explanations in chapter 3. Please revise.', 'pending'),
('rev-003', 'doc-004', 'sup-003', '2024-02-01 14:20:00', 'Outstanding analysis with comprehensive data visualization. Highly recommended.', 'approved'),
('rev-004', 'doc-005', 'sup-001', '2024-02-10 09:45:00', 'Safety protocols section is incomplete. Please add more detailed safety measures before resubmission.', 'rejected');

-- =========================================
-- 6. INSERT SAMPLE DOWNLOADS
-- =========================================
INSERT INTO downloads (id, document_id, user_id, download_timestamp, ip_address) VALUES
('down-001', 'doc-001', 'student-002', '2024-01-25 10:15:00', '192.168.1.100'),
('down-002', 'doc-001', 'staff-002', '2024-01-26 14:30:00', '192.168.1.101'),
('down-003', 'doc-004', 'student-003', '2024-02-05 09:45:00', '192.168.1.102'),
('down-004', 'doc-001', 'student-004', '2024-02-10 16:20:00', '192.168.1.103'),
('down-005', 'doc-004', 'student-005', '2024-02-15 11:30:00', '192.168.1.104');

-- =========================================
-- 7. INSERT SAMPLE COLLABORATORS
-- =========================================
INSERT INTO document_collaborators (id, document_id, user_id, role, approved) VALUES
('collab-001', 'doc-001', 'staff-001', 'co-author', TRUE),
('collab-002', 'doc-003', 'student-001', 'collaborator', TRUE),
('collab-003', 'doc-004', 'staff-002', 'co-author', FALSE);

-- =========================================
-- 8. INSERT SAMPLE AUDIT LOGS
-- =========================================
INSERT INTO audit_logs (id, user_id, action, document_id, details, ip_address, timestamp) VALUES
('audit-001', 'student-001', 'upload', 'doc-001', '{"file_size": 2048576, "file_type": "pdf"}', '192.168.1.100', '2024-01-15 10:30:00'),
('audit-002', 'sup-001', 'approve', 'doc-001', '{"previous_status": "under_review", "new_status": "approved"}', '192.168.1.110', '2024-01-20 15:30:00'),
('audit-003', 'student-002', 'download', 'doc-001', '{"download_method": "direct"}', '192.168.1.100', '2024-01-25 10:15:00'),
('audit-004', 'student-003', 'upload', 'doc-002', '{"file_size": 1536000, "file_type": "pdf"}', '192.168.1.105', '2024-02-20 14:45:00'),
('audit-005', 'sup-001', 'reject', 'doc-005', '{"previous_status": "under_review", "new_status": "rejected", "reason": "Incomplete safety protocols"}', '192.168.1.110', '2024-02-10 09:45:00');

-- =========================================
-- VERIFICATION QUERIES
-- =========================================

-- Check total counts
SELECT 
    'Departments' as entity, COUNT(*) as count FROM departments
UNION ALL
SELECT 'Users', COUNT(*) FROM users
UNION ALL  
SELECT 'Documents', COUNT(*) FROM documents
UNION ALL
SELECT 'Reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'Downloads', COUNT(*) FROM downloads
UNION ALL
SELECT 'Audit Logs', COUNT(*) FROM audit_logs;

-- Check user distribution by role
SELECT role, COUNT(*) as count 
FROM users 
GROUP BY role;

-- Check document status distribution
SELECT status, COUNT(*) as count 
FROM documents 
GROUP BY status;
