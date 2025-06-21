-- =========================================
-- Academic Research Repository System
-- Business Rules Demonstration Queries
-- Database Management System Course Project
-- =========================================

USE academic_repo_db;

-- =========================================
-- BUSINESS RULE DEMONSTRATIONS
-- =========================================

-- ============================================
-- Rule 1: Each user must be assigned exactly one role
-- ============================================
SELECT 
    'User Role Distribution' as check_description,
    role,
    COUNT(*) as user_count
FROM users 
GROUP BY role
ORDER BY role;

-- ============================================
-- Rule 2: Students and staff can upload documents
-- ============================================
SELECT 
    'Document Uploaders by Role' as check_description,
    u.role,
    COUNT(d.id) as documents_uploaded
FROM users u
LEFT JOIN documents d ON u.id = d.uploader_id
WHERE u.role IN ('student', 'staff')
GROUP BY u.role;

-- ============================================
-- Rule 3: Only supervisors can approve/reject documents
-- ============================================
SELECT 
    'Reviews by Supervisor' as check_description,
    u.name as supervisor_name,
    u.specialization_area,
    COUNT(r.id) as reviews_made,
    COUNT(CASE WHEN r.decision = 'approved' THEN 1 END) as approved,
    COUNT(CASE WHEN r.decision = 'rejected' THEN 1 END) as rejected
FROM users u
LEFT JOIN reviews r ON u.id = r.reviewer_id
WHERE u.role = 'supervisor'
GROUP BY u.id, u.name, u.specialization_area;

-- ============================================
-- Rule 4: Each document must have unique title per uploader
-- ============================================
SELECT 
    'Document Title Uniqueness Check' as check_description,
    u.name as uploader,
    d.title,
    COUNT(*) as occurrence_count
FROM documents d
JOIN users u ON d.uploader_id = u.id
GROUP BY d.uploader_id, d.title
HAVING COUNT(*) > 1;  -- This should return empty if rule is enforced

-- ============================================
-- Rule 5: Complete metadata required for all documents
-- ============================================
SELECT 
    'Documents with Complete Metadata' as check_description,
    d.title,
    CASE 
        WHEN dm.keywords IS NOT NULL 
             AND dm.publication_year IS NOT NULL 
             AND dm.authors IS NOT NULL 
        THEN 'Complete'
        ELSE 'Incomplete'
    END as metadata_status
FROM documents d
LEFT JOIN document_metadata dm ON d.id = dm.document_id;

-- ============================================
-- Rule 6: Rejected documents must have rejection reason
-- ============================================
SELECT 
    'Rejected Documents with Reasons' as check_description,
    d.title,
    d.status,
    CASE 
        WHEN d.status = 'rejected' AND d.rejection_reason IS NOT NULL 
        THEN 'Has Reason'
        WHEN d.status = 'rejected' AND d.rejection_reason IS NULL 
        THEN 'Missing Reason'
        ELSE 'Not Applicable'
    END as rejection_reason_status
FROM documents d
WHERE d.status = 'rejected';

-- ============================================
-- Rule 7: Only approved documents are available for download
-- ============================================
SELECT 
    'Downloads of Approved Documents Only' as check_description,
    d.title,
    d.status,
    COUNT(dl.id) as download_count
FROM documents d
LEFT JOIN downloads dl ON d.id = dl.document_id
GROUP BY d.id, d.title, d.status
HAVING COUNT(dl.id) > 0;

-- ============================================
-- Rule 8: Each document linked to exactly one department
-- ============================================
SELECT 
    'Documents per Department' as check_description,
    dept.name as department,
    dept.faculty,
    COUNT(d.id) as document_count
FROM departments dept
LEFT JOIN documents d ON dept.id = d.department_id
GROUP BY dept.id, dept.name, dept.faculty
ORDER BY document_count DESC;

-- ============================================
-- Rule 9: Supervisors only review documents from their department
-- ============================================
SELECT 
    'Supervisor Department Alignment Check' as check_description,
    u.name as supervisor,
    u.assigned_department,
    dept.name as supervisor_dept_name,
    d.department_id as document_dept,
    d.title as document_title,
    CASE 
        WHEN u.assigned_department = d.department_id THEN 'Aligned'
        ELSE 'Misaligned'
    END as alignment_status
FROM reviews r
JOIN users u ON r.reviewer_id = u.id
JOIN documents d ON r.document_id = d.id
LEFT JOIN departments dept ON u.assigned_department = dept.id
WHERE u.role = 'supervisor';

-- ============================================
-- Rule 10: All key actions must be logged
-- ============================================
SELECT 
    'Action Logging Coverage' as check_description,
    al.action,
    COUNT(*) as log_count,
    COUNT(DISTINCT al.user_id) as unique_users,
    MIN(al.timestamp) as first_occurrence,
    MAX(al.timestamp) as last_occurrence
FROM audit_logs al
GROUP BY al.action
ORDER BY log_count DESC;

-- ============================================
-- ADVANCED QUERIES FOR PRESENTATION
-- ============================================

-- Most Active Users (Upload and Download Activity)
SELECT 
    'Most Active Users' as report_type,
    u.name,
    u.role,
    dept.name as department,
    COUNT(DISTINCT d.id) as documents_uploaded,
    COUNT(DISTINCT dl.id) as downloads_made,
    COUNT(DISTINCT r.id) as reviews_made
FROM users u
JOIN departments dept ON u.department_id = dept.id
LEFT JOIN documents d ON u.id = d.uploader_id
LEFT JOIN downloads dl ON u.id = dl.user_id
LEFT JOIN reviews r ON u.id = r.reviewer_id
GROUP BY u.id, u.name, u.role, dept.name
HAVING (documents_uploaded > 0 OR downloads_made > 0 OR reviews_made > 0)
ORDER BY (documents_uploaded + downloads_made + reviews_made) DESC
LIMIT 10;

-- Department Performance Summary
SELECT 
    'Department Performance' as report_type,
    dept.name as department,
    dept.faculty,
    COUNT(DISTINCT u.id) as total_users,
    COUNT(DISTINCT d.id) as total_documents,
    COUNT(DISTINCT CASE WHEN d.status = 'approved' THEN d.id END) as approved_docs,
    COUNT(DISTINCT CASE WHEN d.status = 'rejected' THEN d.id END) as rejected_docs,
    ROUND(
        COUNT(DISTINCT CASE WHEN d.status = 'approved' THEN d.id END) * 100.0 / 
        NULLIF(COUNT(DISTINCT d.id), 0), 2
    ) as approval_rate_percent
FROM departments dept
LEFT JOIN users u ON dept.id = u.department_id
LEFT JOIN documents d ON dept.id = d.department_id
GROUP BY dept.id, dept.name, dept.faculty
ORDER BY total_documents DESC;

-- Document Popularity (Most Downloaded)
SELECT 
    'Most Popular Documents' as report_type,
    d.title,
    u.name as uploader,
    dept.name as department,
    d.status,
    d.download_count,
    COUNT(dl.id) as actual_downloads,
    dm.keywords
FROM documents d
JOIN users u ON d.uploader_id = u.id
JOIN departments dept ON d.department_id = dept.id
LEFT JOIN downloads dl ON d.id = dl.document_id
LEFT JOIN document_metadata dm ON d.id = dm.document_id
GROUP BY d.id, d.title, u.name, dept.name, d.status, d.download_count, dm.keywords
ORDER BY d.download_count DESC
LIMIT 10;

-- Review Efficiency (Supervisor Performance)
SELECT 
    'Supervisor Review Performance' as report_type,
    u.name as supervisor,
    u.specialization_area,
    dept.name as department,
    COUNT(r.id) as total_reviews,
    COUNT(CASE WHEN r.decision = 'approved' THEN 1 END) as approved,
    COUNT(CASE WHEN r.decision = 'rejected' THEN 1 END) as rejected,
    COUNT(CASE WHEN r.decision = 'pending' THEN 1 END) as pending,
    ROUND(AVG(DATEDIFF(r.review_date, d.upload_date)), 2) as avg_review_time_days
FROM users u
JOIN departments dept ON u.department_id = dept.id
LEFT JOIN reviews r ON u.id = r.reviewer_id
LEFT JOIN documents d ON r.document_id = d.id
WHERE u.role = 'supervisor'
GROUP BY u.id, u.name, u.specialization_area, dept.name
ORDER BY total_reviews DESC;

-- System Usage Timeline
SELECT 
    'System Usage Timeline' as report_type,
    DATE(al.timestamp) as date,
    al.action,
    COUNT(*) as action_count
FROM audit_logs al
WHERE al.timestamp >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
GROUP BY DATE(al.timestamp), al.action
ORDER BY date DESC, action_count DESC;

-- User Engagement Score
SELECT 
    'User Engagement Score' as report_type,
    u.name,
    u.role,
    dept.name as department,
    COUNT(DISTINCT d.id) * 3 + 
    COUNT(DISTINCT dl.id) * 1 + 
    COUNT(DISTINCT r.id) * 2 as engagement_score,
    CASE 
        WHEN COUNT(DISTINCT d.id) * 3 + COUNT(DISTINCT dl.id) * 1 + COUNT(DISTINCT r.id) * 2 >= 10 THEN 'High'
        WHEN COUNT(DISTINCT d.id) * 3 + COUNT(DISTINCT dl.id) * 1 + COUNT(DISTINCT r.id) * 2 >= 5 THEN 'Medium'
        ELSE 'Low'
    END as engagement_level
FROM users u
JOIN departments dept ON u.department_id = dept.id
LEFT JOIN documents d ON u.id = d.uploader_id
LEFT JOIN downloads dl ON u.id = dl.user_id
LEFT JOIN reviews r ON u.id = r.reviewer_id
GROUP BY u.id, u.name, u.role, dept.name
ORDER BY engagement_score DESC;
