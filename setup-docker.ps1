# Simple Docker Setup - No MySQL installation required
Write-Host "🚀 Starting Academic Repository System with Docker..." -ForegroundColor Green

# Check if Docker is available
try {
    $null = Get-Command docker -ErrorAction Stop
    Write-Host "✅ Docker found" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed or not running" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

Write-Host "🐳 Starting MySQL database with Docker..." -ForegroundColor Cyan
docker-compose up -d mysql

Write-Host "⏳ Waiting for MySQL to initialize (30 seconds)..." -ForegroundColor Yellow
Start-Sleep 30

Write-Host "✅ Database should be ready!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Database Information:" -ForegroundColor Cyan
Write-Host "   Database: academic_repo_db" -ForegroundColor White
Write-Host "   Username: academic_user" -ForegroundColor White
Write-Host "   Password: academic_pass" -ForegroundColor White
Write-Host "   Host: localhost" -ForegroundColor White
Write-Host "   Port: 3306" -ForegroundColor White
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Test connection: python test-database.py" -ForegroundColor White
Write-Host "   2. Start backend: cd backend && uvicorn main:app --reload" -ForegroundColor White
Write-Host "   3. Start frontend: cd frontend && npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Useful commands:" -ForegroundColor Yellow
Write-Host "   Stop: docker-compose down" -ForegroundColor White
Write-Host "   Logs: docker-compose logs mysql" -ForegroundColor White
