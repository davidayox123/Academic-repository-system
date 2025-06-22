# Academic Repository System - Database Setup Guide

This guide provides all the SQL commands and database setup instructions for the Academic Repository System.

## Table of Contents
- [Database Setup from Scratch](#database-setup-from-scratch)
- [Database Management Commands](#database-management-commands)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Database Setup from Scratch

### 1. Install MySQL (if not already installed)

**Windows:**
```powershell
# Download MySQL installer from https://dev.mysql.com/downloads/installer/
# Or use chocolatey
choco install mysql

# Or use winget
winget install Oracle.MySQL
```

### 2. Start MySQL Service

**Windows:**
```powershell
# Start MySQL service
net start mysql

# Or using services
services.msc
# Find "MySQL80" service and start it
```

### 3. Initial MySQL Setup

```sql
-- Connect to MySQL as root (you'll be prompted for password)
mysql -u root -p

-- Create the database
CREATE DATABASE academic_repo_db;

-- Create a dedicated user (optional but recommended)
CREATE USER 'academic_user'@'localhost' IDENTIFIED BY 'academic_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON academic_repo_db.* TO 'academic_user'@'localhost';
FLUSH PRIVILEGES;

-- Verify database creation
SHOW DATABASES;

-- Use the database
USE academic_repo_db;
```

### 4. Database Configuration in Backend

Update your `backend/app/core/config.py`:

```python
# Option 1: Using root user (current setup)
DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/academic_repo_db"

# Option 2: Using dedicated user (recommended)
DATABASE_URL: str = "mysql+pymysql://academic_user:academic_password@localhost:3306/academic_repo_db"
```

### 5. Verify Connection

```sql
-- Test connection
mysql -u root -p academic_repo_db

-- Or with dedicated user
mysql -u academic_user -p academic_repo_db

-- Once connected, check if database is empty
SHOW TABLES;
```

### 6. Environment Variables (Optional)

Create `.env` file in backend directory:
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/academic_repo_db
DATABASE_ECHO=False
SECRET_KEY=your-super-secret-key-change-this-in-production
```

### 7. Initialize with Sample Data

Once your backend starts, it will automatically:
1. Create all tables using SQLAlchemy
2. Populate with sample data via `init_sample_data()`

## Database Management Commands

### Basic Connection & Navigation

```sql
-- Connect to MySQL (you'll be prompted for password)
mysql -u root -p

-- Show all databases
SHOW DATABASES;

-- Use the academic repository database
USE academic_repo_db;

-- Show all tables in the database
SHOW TABLES;
```

### Table Structure Commands

```sql
-- Check table structure for all main tables
DESCRIBE users;
DESCRIBE departments; 
DESCRIBE documents;
DESCRIBE reviews;
DESCRIBE activity_logs;
DESCRIBE downloads;
```

### Data Verification Commands

```sql
-- View sample data
SELECT * FROM users;
SELECT * FROM departments;
SELECT * FROM documents;

-- Count records in tables
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM departments;
SELECT COUNT(*) FROM documents;

-- View limited records
SELECT id, name, email, role FROM users LIMIT 5;
SELECT id, name, code, faculty FROM departments;
SELECT id, title, status, author_id FROM documents LIMIT 5;
```

### Relationship Queries

```sql
-- Check foreign key relationships
SELECT 
    u.name as user_name, 
    u.role, 
    d.name as department_name 
FROM users u 
LEFT JOIN departments d ON u.department_id = d.id;

-- View document statistics
SELECT 
    status, 
    COUNT(*) as count 
FROM documents 
GROUP BY status;
```

### Database Reset Commands

```sql
-- Complete database reset (used to fix schema conflicts)
DROP DATABASE IF EXISTS academic_repo_db;
CREATE DATABASE academic_repo_db;

-- Quick reset via command line
mysql -u root -p -e "DROP DATABASE IF EXISTS academic_repo_db; CREATE DATABASE academic_repo_db;"
```

## Configuration

### Database Connection Details

Your MySQL connection details (from your backend config):
- **Host**: localhost
- **Port**: 3306 
- **Username**: root
- **Password**: password (your MySQL root password)
- **Database**: academic_repo_db

### Backend Configuration

Your current setup uses these settings in `backend/app/core/config.py`:

```python
class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/academic_repo_db"
    DATABASE_ECHO: bool = False
    
    # Connection pool settings (improved for stability)
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
```

## Troubleshooting

### Common Issues and Solutions

#### 1. "Unknown column" errors
```sql
-- Solution: Reset the database completely
DROP DATABASE IF EXISTS academic_repo_db;
CREATE DATABASE academic_repo_db;
-- Then restart your backend
```

#### 2. Connection pool exhausted
This was fixed by updating the database configuration with larger pool sizes.

#### 3. File upload "422 Unprocessable Entity"
Fixed by ensuring proper form data fields and backend validation.

#### 4. WebSocket connection loops
Resolved by improving connection management and reconnection logic.

### Backup and Restore

```bash
# Create backup
mysqldump -u root -p academic_repo_db > academic_repo_backup.sql

# Restore from backup
mysql -u root -p academic_repo_db < academic_repo_backup.sql
```

### Verification After Setup

```sql
-- After backend startup, verify everything works
USE academic_repo_db;
SHOW TABLES;

-- Check sample data exists
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM departments;
SELECT COUNT(*) FROM documents;

-- View sample users with their roles
SELECT id, name, email, role FROM users;

-- Check departments are created
SELECT id, name, code, faculty FROM departments;
```

## Key Commands Used During Development

### The Critical Fix Command
This command resolved the major schema conflict issue:
```sql
mysql -u root -p -e "DROP DATABASE IF EXISTS academic_repo_db; CREATE DATABASE academic_repo_db;"
```

### Testing API Connection
```powershell
# Test if backend API is working
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/dashboard/stats?role=student" -Method GET
```

## Next Steps

1. **Run the database setup commands above**
2. **Start your backend**: `cd backend && uvicorn main:app --reload`
3. **Start your frontend**: `cd frontend && npm run dev`
4. **Verify functionality**: Test user role switching, file uploads, and dashboard

The Academic Repository System will automatically:
- Create all necessary database tables
- Populate with sample data (users, departments, documents)
- Set up proper relationships and constraints
- Initialize the system for immediate use

Your database is now ready for the Academic Repository System!
