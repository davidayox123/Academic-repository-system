@echo off
echo 🎓 Setting up Academic Repository System...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create uploads directory
echo 📁 Creating uploads directory...
if not exist uploads mkdir uploads

REM Copy environment file
echo ⚙️ Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo ✅ Created .env file from .env.example
    echo ⚠️  Please update the .env file with your configuration
) else (
    echo ✅ .env file already exists
)

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
cd frontend
call npm install
cd ..

REM Install backend dependencies (if running without Docker)
echo 🐍 Setting up Python backend...
cd backend
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo ✅ Backend dependencies installed
) else (
    echo ⚠️  Python not found. Backend will run in Docker container.
)
cd ..

REM Start the services
echo 🚀 Starting services with Docker Compose...
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are running
echo 🔍 Checking service status...
docker-compose ps

echo.
echo 🎉 Academic Repository System is now running!
echo.
echo 📍 Access points:
echo    - Frontend: http://localhost:5173
echo    - Backend API: http://localhost:8000
echo    - API Documentation: http://localhost:8000/docs
echo    - MySQL: localhost:3306
echo.
echo 👥 Default login credentials:
echo    - Admin: admin@university.edu / password123
echo    - Supervisor: supervisor@university.edu / password123
echo    - Student: student@university.edu / password123
echo.
echo ⚠️  Remember to change default passwords in production!
echo.
echo 🛠️  To stop the services: docker-compose down
echo 🔧  To view logs: docker-compose logs -f
echo.
pause
