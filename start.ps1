# Academic Repository System - Quick Start Script
# This script starts the entire development environment

param(
    [switch]$Setup,
    [switch]$Test,
    [switch]$Clean
)

Write-Host "🚀 Academic Repository System - Quick Start" -ForegroundColor Green
Write-Host "=" * 50

function Install-Dependencies {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
    
    # Install backend dependencies
    Write-Host "Installing Python dependencies..."
    Set-Location backend
    pip install -r requirements.txt
    Set-Location ..
    
    # Install frontend dependencies
    Write-Host "Installing Node.js dependencies..."
    Set-Location frontend
    npm install
    Set-Location ..
    
    Write-Host "✅ Dependencies installed!" -ForegroundColor Green
}

function Setup-Database {
    Write-Host "🗄️ Setting up database..." -ForegroundColor Cyan
    
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        Write-Host "Starting MySQL with Docker..."
        docker-compose up -d mysql
        Start-Sleep 10
    } else {
        Write-Host "Running database setup script..."
        powershell -ExecutionPolicy Bypass -File setup-database.ps1
    }
}

function Test-System {
    Write-Host "🧪 Testing system..." -ForegroundColor Cyan
    
    Write-Host "Testing database connection..."
    python test-database.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Database test passed!" -ForegroundColor Green
    } else {
        Write-Host "Database test failed!" -ForegroundColor Red
        return $false
    }
    
    return $true
}

function Start-Services {
    Write-Host "🚀 Starting services..." -ForegroundColor Cyan
    
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        Write-Host "Starting with Docker Compose..."
        docker-compose up -d
        Start-Sleep 5
    } else {
        Write-Host "Starting services manually..."
        
        # Start backend
        Write-Host "Starting backend server..."
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; uvicorn main:app --reload --host 0.0.0.0 --port 8000"
        
        Start-Sleep 3
        
        # Start frontend
        Write-Host "Starting frontend server..."
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
    }
    
    Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
    Start-Sleep 10
}

function Show-Info {
    Write-Host ""
    Write-Host "🎉 Academic Repository System is ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 Application URLs:" -ForegroundColor Cyan
    Write-Host "   Frontend: http://localhost:5173" -ForegroundColor White
    Write-Host "   Backend API: http://localhost:8000/docs" -ForegroundColor White
    Write-Host "   Database: localhost:3306" -ForegroundColor White
    Write-Host ""
    Write-Host "👥 Test Accounts:" -ForegroundColor Cyan
    Write-Host "   Admin: admin@university.edu / password123" -ForegroundColor White
    Write-Host "   Supervisor: supervisor@university.edu / password123" -ForegroundColor White
    Write-Host "   Student: student@university.edu / password123" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 Useful Commands:" -ForegroundColor Cyan
    Write-Host "   Test integration: python test-integration.py" -ForegroundColor White
    Write-Host "   Stop services: docker-compose down" -ForegroundColor White
    Write-Host "   View logs: docker-compose logs -f" -ForegroundColor White
}

function Clean-Environment {
    Write-Host "🧹 Cleaning environment..." -ForegroundColor Cyan
    
    docker-compose down -v
    docker system prune -f
    
    Remove-Item -Recurse -Force backend/__pycache__ -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force frontend/node_modules -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force frontend/dist -ErrorAction SilentlyContinue
    
    Write-Host "✅ Environment cleaned!" -ForegroundColor Green
}

# Main execution
try {
    if ($Clean) {
        Clean-Environment
        exit 0
    }
    
    if ($Setup) {
        Install-Dependencies
        Setup-Database
        
        if (Test-System) {
            Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Setup failed during testing!" -ForegroundColor Red
            exit 1
        }
        exit 0
    }
    
    if ($Test) {
        if (Test-System) {
            Write-Host "Running integration tests..."
            python test-integration.py
        }
        exit 0
    }
    
    # Default: Start the application
    Setup-Database
    Start-Services
    
    # Test if everything is working
    Write-Host "🧪 Running quick integration test..." -ForegroundColor Cyan
    python test-integration.py
    
    if ($LASTEXITCODE -eq 0) {
        Show-Info
    } else {
        Write-Host "⚠️ Some services may not be ready yet. Please wait a moment and try again." -ForegroundColor Yellow
        Show-Info
    }
    
} catch {
    Write-Host "❌ An error occurred: $_" -ForegroundColor Red
    Write-Host "💡 Try running with -Setup flag first: ./start.ps1 -Setup" -ForegroundColor Yellow
    exit 1
}
