@echo off
echo ================================================================
echo  Academic Repository System - Quick Start for Friends
echo ================================================================
echo.

echo [1/4] Checking prerequisites...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)
echo ✅ Python is installed

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)
echo ✅ Node.js is installed

REM Check if MySQL is running
echo [2/4] Checking MySQL connection...
mysql -u root -p -e "SELECT 1;" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Cannot connect to MySQL
    echo Please make sure MySQL is running and you have the correct password
    echo You can start MySQL through XAMPP, WAMP, or MySQL Service
    pause
    exit /b 1
)
echo ✅ MySQL is accessible

echo.
echo [3/4] Setting up database...
echo.

REM Setup database
mysql -u root -p < database\simple_schema.sql
if %errorlevel% neq 0 (
    echo ❌ Failed to create database schema
    pause
    exit /b 1
)

mysql -u root -p < database\sample_data.sql
if %errorlevel% neq 0 (
    echo ❌ Failed to load sample data
    pause
    exit /b 1
)

echo ✅ Database setup complete!
echo.

echo [4/4] Installing dependencies...
echo.

cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)
cd ..

cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)
cd ..

echo ✅ All dependencies installed!
echo.
echo ================================================================
echo  🎉 Setup Complete! Now starting the system...
echo ================================================================
echo.
echo The system will start in 3 separate windows:
echo 1. Backend Server (FastAPI)
echo 2. Frontend Server (React)
echo 3. This status window
echo.
echo ⏰ Please wait a moment for both servers to start...
echo.

REM Start backend in new window
start "Academic Repository - Backend" cmd /k "cd backend && uvicorn main:app --reload --host 127.0.0.1 --port 8000"

REM Wait a bit for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend in new window
start "Academic Repository - Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ================================================================
echo  🚀 System Started Successfully!
echo ================================================================
echo.
echo 🌐 Frontend: http://localhost:5173
echo 📊 Backend API: http://localhost:8000/docs
echo 🗄️  Database: localhost:3306
echo.
echo 👥 Test Accounts:
echo.
echo 📧 Admin: admin@university.edu (password: password123)
echo 📧 Supervisor: supervisor1@university.edu (password: password123)  
echo 📧 Student: alice.johnson@student.edu (password: password123)
echo.
echo ================================================================
echo.
echo ✨ The system is ready for demonstration!
echo.
echo 💡 Tips:
echo • Login with different accounts to see role-based features
echo • Try uploading a document as a student
echo • Review documents as a supervisor
echo • Check audit logs as an admin
echo.
echo Press any key to keep this window open...
pause >nul
