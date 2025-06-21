# Academic Repository System - Quick Start for Friends
# PowerShell version for better Windows compatibility

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " Academic Repository System - Quick Start for Friends" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

Write-Host "[1/4] Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check Python
if (Test-Command "python") {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python is installed: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Node.js
if (Test-Command "node") {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js is installed: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check MySQL
Write-Host "[2/4] Checking MySQL connection..." -ForegroundColor Yellow
Write-Host ""

mysql -u root -e "SELECT 1;" 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ MySQL is accessible" -ForegroundColor Green
} else {
    Write-Host "❌ Cannot connect to MySQL" -ForegroundColor Red
    Write-Host "Please make sure MySQL is running and you have the correct password" -ForegroundColor Red
    Write-Host "You can start MySQL through XAMPP, WAMP, or MySQL Service" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[3/4] Setting up database..." -ForegroundColor Yellow
Write-Host ""

# Setup database schema
mysql -u root -p -e "source database/simple_schema.sql"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create database schema" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Load sample data
mysql -u root -p -e "source database/sample_data.sql"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to load sample data" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Database setup complete!" -ForegroundColor Green
Write-Host ""

Write-Host "[4/4] Installing dependencies..." -ForegroundColor Yellow
Write-Host ""

# Install backend dependencies
Set-Location backend
pip install -r requirements.txt | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install backend dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Set-Location ..

# Install frontend dependencies
Set-Location frontend
npm install | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install frontend dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Set-Location ..

Write-Host "✅ All dependencies installed!" -ForegroundColor Green
Write-Host ""

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " 🎉 Setup Complete! Now starting the system..." -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "The system will start in 3 separate windows:" -ForegroundColor White
Write-Host "1. Backend Server (FastAPI)" -ForegroundColor White
Write-Host "2. Frontend Server (React)" -ForegroundColor White
Write-Host "3. This status window" -ForegroundColor White
Write-Host ""
Write-Host "⏰ Please wait a moment for both servers to start..." -ForegroundColor Yellow
Write-Host ""

# Start backend in new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; uvicorn main:app --reload --host 127.0.0.1 --port 8000"

# Wait for backend to start
Start-Sleep -Seconds 5

# Start frontend in new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"

# Wait for frontend to start
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " 🚀 System Started Successfully!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🌐 Frontend: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:5173" -ForegroundColor Cyan
Write-Host "📊 Backend API: " -NoNewline -ForegroundColor White  
Write-Host "http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🗄️ Database: " -NoNewline -ForegroundColor White
Write-Host "localhost:3306" -ForegroundColor Cyan
Write-Host ""

Write-Host "👥 Test Accounts:" -ForegroundColor Yellow
Write-Host ""
Write-Host "📧 Admin: " -NoNewline -ForegroundColor White
Write-Host "admin@university.edu " -NoNewline -ForegroundColor Cyan
Write-Host "(password: password123)" -ForegroundColor Gray

Write-Host "📧 Supervisor: " -NoNewline -ForegroundColor White
Write-Host "supervisor1@university.edu " -NoNewline -ForegroundColor Cyan
Write-Host "(password: password123)" -ForegroundColor Gray

Write-Host "📧 Student: " -NoNewline -ForegroundColor White
Write-Host "alice.johnson@student.edu " -NoNewline -ForegroundColor Cyan
Write-Host "(password: password123)" -ForegroundColor Gray

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✨ The system is ready for demonstration!" -ForegroundColor Green
Write-Host ""

Write-Host "💡 Tips:" -ForegroundColor Yellow
Write-Host "• Login with different accounts to see role-based features" -ForegroundColor White
Write-Host "• Try uploading a document as a student" -ForegroundColor White
Write-Host "• Review documents as a supervisor" -ForegroundColor White
Write-Host "• Check audit logs as an admin" -ForegroundColor White
Write-Host ""

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to keep this window open"
