# Academic Repository System - SQL Documentation

## Project Overview
This Academic Repository System uses MySQL database to manage:
- Users (students, staff, supervisors, admins)
- Documents (research papers, assignments, theses)
- Departments 
- Reviews and approvals
- Activity logs and downloads

## Database Setup Commands

### 1. Create Database
```sql
-- Connect to MySQL
mysql -u root -p

-- Create the main database
CREATE DATABASE academic_repo_db;

-- Use the database
USE academic_repo_db;

-- Verify creation
SHOW DATABASES;
```

### 2. Check Tables (After Backend Startup)
```sql
-- See all tables created by the system
SHOW TABLES;

-- Output should show:
-- +---------------------------+
-- | Tables_in_academic_repo_db|
-- +---------------------------+
-- | activity_logs             |
-- | departments               |
-- | documents                 |
-- | downloads                 |
-- | reviews                   |
-- | users                     |
-- +---------------------------+
```

### 3. View Table Structures
```sql
-- Check users table structure
DESCRIBE users;

-- Check documents table structure  
DESCRIBE documents;

-- Check departments table structure
DESCRIBE departments;

-- Check reviews table structure
DESCRIBE reviews;
```

### 4. Sample Data Queries

#### View Users
```sql
-- See all users
SELECT id, name, email, role, created_at FROM users;

-- Count users by role
SELECT role, COUNT(*) as count FROM users GROUP BY role;
```

#### View Documents
```sql
-- See all documents
SELECT id, title, status, upload_date, uploader_id FROM documents;

-- Count documents by status
SELECT status, COUNT(*) as count FROM documents GROUP BY status;
```

#### View Departments
```sql
-- See all departments
SELECT * FROM departments;
```

## Database Schema Explanation

### Tables and Relationships

1. **users** - Stores all system users
   - Primary Key: id (UUID)
   - Roles: student, staff, supervisor, admin
   - Foreign Key: department_id (links to departments)

2. **departments** - Academic departments
   - Primary Key: id (UUID)
   - Contains: Computer Science, Physics, Environmental Science

3. **documents** - Uploaded academic documents
   - Primary Key: id (UUID)
   - Foreign Keys: uploader_id (user), supervisor_id (user), department_id
   - Status: pending, under_review, approved, rejected

4. **reviews** - Document review/approval records
   - Links documents to reviewers
   - Contains approval/rejection decisions

5. **downloads** - Track document download history
   - Logs who downloaded what and when

6. **activity_logs** - System audit trail
   - Records all important user actions

## Key SQL Operations Used

### Data Definition Language (DDL)
- CREATE DATABASE - Creates the database
- CREATE TABLE - Creates tables (done by SQLAlchemy)
- ALTER TABLE - Modifies table structure
- DROP TABLE - Removes tables

### Data Manipulation Language (DML)
- INSERT - Adds new records (users, documents, etc.)
- UPDATE - Modifies existing records (document status)
- DELETE - Removes records
- SELECT - Retrieves data for display

### Data Query Language (DQL)
- SELECT with JOIN - Combines data from multiple tables
- WHERE clauses - Filters data
- GROUP BY - Aggregates data
- ORDER BY - Sorts results

## Backup and Restore Commands

### Backup Database
```sql
-- Create backup
mysqldump -u root -p academic_repo_db > academic_repo_backup.sql
```

### Restore Database
```sql
-- Restore from backup
mysql -u root -p academic_repo_db < academic_repo_backup.sql
```

## Performance Indexes

The system uses indexes on:
- user emails (for fast login lookup)
- document status (for filtering)
- upload dates (for sorting)
- department relationships (for joins)

## Explanation for Presentation

**What is this database doing?**
1. Stores academic users with different roles and permissions
2. Manages document uploads with approval workflows
3. Tracks document reviews and download history
4. Maintains audit logs for compliance
5. Organizes users by academic departments

**Why MySQL?**
- Reliable and widely used
- Good performance for this size of data
- ACID compliance for data integrity
- Good integration with Python/FastAPI

**Key Features Demonstrated:**
- Relational database design with foreign keys
- User role-based access control
- Document workflow management
- Activity logging and audit trails
- File metadata storage

## Using MySQL Workbench Instead of Terminal

### Step 1: Open MySQL Workbench
1. Open MySQL Workbench application
2. Create a new connection or use existing one
3. Connect to your MySQL server (localhost:3306)

### Step 2: Create Database Using Workbench
```sql
-- Execute these commands one by one in MySQL Workbench
CREATE DATABASE academic_repository;
USE academic_repository;
```

### Step 3: Execute the Database Schema
1. Open the file `database/init.sql` in MySQL Workbench
2. Or copy and paste all the SQL commands below:

```sql
-- Copy all the CREATE TABLE commands from init.sql
-- Execute them in MySQL Workbench Query Editor
```

### Step 4: Verify Database Creation
```sql
-- Check if database exists
SHOW DATABASES;

-- Use the database
USE academic_repository;

-- Show all tables
SHOW TABLES;

-- Check table structure
DESCRIBE users;
DESCRIBE documents;
DESCRIBE departments;
DESCRIBE reviews;
DESCRIBE activity_logs;
DESCRIBE downloads;
```

### Screenshots to Take for Documentation:
1. **MySQL Workbench Main Screen** - showing connection
2. **Database Creation** - showing CREATE DATABASE command execution
3. **Tables List** - showing all created tables with SHOW TABLES
4. **Table Structure** - showing DESCRIBE commands for main tables
5. **Sample Data** - showing SELECT * FROM users; and SELECT * FROM documents;

### Sample Queries to Demonstrate:
```sql
-- Show all users
SELECT id, name, email, role, created_at FROM users;

-- Show all documents with uploader names
SELECT d.title, d.filename, d.status, u.name as uploader_name 
FROM documents d 
JOIN users u ON d.uploader_id = u.id;

-- Show documents by department
SELECT d.title, dept.name as department_name, d.upload_date
FROM documents d 
JOIN users u ON d.uploader_id = u.id
JOIN departments dept ON u.department_id = dept.id;

-- Count documents by status
SELECT status, COUNT(*) as count 
FROM documents 
GROUP BY status;

-- Show user roles distribution
SELECT role, COUNT(*) as count 
FROM users 
GROUP BY role;
```

### For Your Presentation - Key SQL Concepts Used:

1. **Data Definition Language (DDL):**
   - CREATE DATABASE
   - CREATE TABLE
   - ALTER TABLE
   - DROP TABLE

2. **Data Manipulation Language (DML):**
   - INSERT INTO
   - UPDATE
   - DELETE
   - SELECT

3. **Database Relationships:**
   - Foreign Keys (FK)
   - One-to-Many relationships
   - Many-to-One relationships

4. **Constraints:**
   - PRIMARY KEY
   - FOREIGN KEY
   - UNIQUE
   - NOT NULL
   - DEFAULT values

5. **MySQL-Specific Features:**
   - AUTO_INCREMENT
   - TIMESTAMP with automatic updates
   - ENUM types
   - UUID data types

### Quick Explanation for Questions:
- **Why MySQL?** Reliable, widely-used, good for academic projects
- **Database Design?** Normalized structure with proper relationships
- **Security?** Foreign key constraints, data validation
- **Performance?** Indexed columns for faster queries
