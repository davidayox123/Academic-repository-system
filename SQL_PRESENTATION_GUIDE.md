# Academic Repository System - SQL Database Documentation

## Overview
This document contains all the SQL commands and database setup for the Academic Repository System project.

## Database Setup Instructions

### Method 1: Using MySQL Workbench (Recommended for Presentation)

**Step 1: Open MySQL Workbench**
- Launch MySQL Workbench application
- Connect to your MySQL server (localhost:3306)

**Step 2: Load and Execute SQL Script**
- File → Open SQL Script
- Navigate to project folder and select `init.sql`
- Click the lightning bolt icon (⚡) or press Ctrl+Shift+Enter to execute

**Step 3: Take Screenshots for Presentation**
- Screenshot 1: Database creation and table creation results
- Screenshot 2: SHOW TABLES output displaying all created tables
- Screenshot 3: Sample data display showing users, documents, departments
- Screenshot 4: Query results demonstrating database functionality

### Method 2: Using Command Line (Alternative)
```bash
# Navigate to project directory
cd c:\Users\USER\Documents\projects\Academic-repository-system

# Execute SQL script
mysql -u root -p < init.sql
```

## What the Database Script Does

### 1. Creates Academic Repository Database
```sql
CREATE DATABASE IF NOT EXISTS academic_repository;
USE academic_repository;
```

### 2. Creates All Required Tables with Relationships
- **departments**: Academic departments (Computer Science, Physics, etc.)
- **users**: Students, staff, supervisors, and admins
- **documents**: Research papers, thesis, assignments, reports
- **reviews**: Document approval/rejection system
- **activity_logs**: System activity tracking
- **downloads**: Document download tracking

### 3. Inserts Sample Data
- 4 departments (Computer Science, Physics, Environmental Science, Mathematics)
- 6 users (1 admin, 1 supervisor, 1 staff, 3 students)
- 4 sample documents with different statuses
- Sample reviews and activity logs

### 4. Shows Results
- Displays all created tables
- Shows sample data from each table
- Provides database statistics

## Database Schema

### Users Table Structure
```sql
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    role ENUM('student', 'staff', 'supervisor', 'admin'),
    department_id CHAR(36) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
```

### Documents Table Structure
```sql
CREATE TABLE documents (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    title VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    category ENUM('research', 'thesis', 'assignment', 'presentation', 'paper', 'report', 'project', 'other'),
    status ENUM('pending', 'under_review', 'approved', 'rejected'),
    uploader_id CHAR(36) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    download_count INT DEFAULT 0,
    FOREIGN KEY (uploader_id) REFERENCES users(id)
);
```

## Key SQL Concepts Demonstrated

### Data Definition Language (DDL)
- **CREATE DATABASE**: Creates the academic repository database
- **CREATE TABLE**: Creates all system tables with proper structure
- **PRIMARY KEY**: Unique identifier for each record
- **FOREIGN KEY**: Establishes relationships between tables
- **ENUM**: Defines allowed values (roles, status, categories)

### Data Manipulation Language (DML)
- **INSERT INTO**: Adds sample data to all tables
- **SELECT**: Retrieves and displays data
- **UPDATE**: Modifies existing records
- **DELETE**: Removes records (with proper constraints)

### Database Relationships
- **One-to-Many**: Department → Users, User → Documents
- **Many-to-One**: Documents → User (uploader), Reviews → User (reviewer)
- **Referential Integrity**: Foreign key constraints maintain data consistency

### MySQL-Specific Features
- **UUID()**: Generates unique identifiers
- **AUTO_INCREMENT**: Automatic ID generation
- **TIMESTAMP**: Automatic date/time tracking
- **ON UPDATE CURRENT_TIMESTAMP**: Automatic update tracking

## Sample Queries for Demonstration

### Show All Users with Departments
```sql
SELECT u.name, u.email, u.role, d.name as department 
FROM users u 
JOIN departments d ON u.department_id = d.id;
```

### Documents by Status
```sql
SELECT status, COUNT(*) as count 
FROM documents 
GROUP BY status;
```

### Recent Document Uploads
```sql
SELECT d.title, u.name as uploader, d.upload_date, d.status
FROM documents d 
JOIN users u ON d.uploader_id = u.id 
ORDER BY d.upload_date DESC;
```

## Database Statistics After Setup
- **Total Users**: 6 (1 admin, 1 supervisor, 1 staff, 3 students)
- **Total Documents**: 4 (various categories and statuses)
- **Total Departments**: 4 (Computer Science, Physics, Environmental Science, Mathematics)
- **Total Reviews**: 2 (approved documents)

## For Presentation Questions - Be Ready to Explain:
1. **Why MySQL?** Industry standard, reliable, supports ACID properties
2. **Database Design**: Normalized structure prevents data redundancy
3. **Security**: Foreign key constraints ensure data integrity
4. **Scalability**: Indexed columns for efficient queries
5. **Real-world Application**: Mirrors actual university document management systems

## Quick Steps for Your Presentation:
1. Open MySQL Workbench and connect to server
2. Execute the `init.sql` script
3. Show the SHOW TABLES result
4. Run a few SELECT queries to show data
5. Explain the relationships between tables
6. Demonstrate how the database supports the web application
