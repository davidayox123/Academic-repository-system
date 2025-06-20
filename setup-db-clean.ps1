# Academic Repository System Database Setup Script
# Clean version with no syntax errors

Write-Host "🚀 Setting up Academic Repository System Database..." -ForegroundColor Green

# Database configuration
$DB_NAME = "academic_repo_db"
$DB_USER = "academic_user"
$DB_PASS = "260307"
$DB_ROOT_PASS = "260307"

# Check if MySQL is available
try {
    $null = Get-Command mysql -ErrorAction Stop
    Write-Host "✅ MySQL found in PATH" -ForegroundColor Green
} catch {
    Write-Host "❌ MySQL is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install MySQL or use Docker:" -ForegroundColor Yellow
    Write-Host "docker-compose up -d mysql" -ForegroundColor Cyan
    exit 1
}

Write-Host "📋 Setting up database and user..." -ForegroundColor Cyan

# Create temporary SQL file to avoid PowerShell parsing issues
$sqlContent = @"
CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE $DB_NAME;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
CREATE USER IF NOT EXISTS '$DB_USER'@'%' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'%';
FLUSH PRIVILEGES;
"@

$tempFile = "setup_temp.sql"

try {
    Write-Host "🔐 Creating SQL script..." -ForegroundColor Yellow
    $sqlContent | Out-File -FilePath $tempFile -Encoding UTF8
    
    Write-Host "🔐 Executing database setup..." -ForegroundColor Yellow
    & mysql -u root -p$DB_ROOT_PASS --execute="source $tempFile"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Database setup completed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Database Information:" -ForegroundColor Cyan
        Write-Host "   Database: $DB_NAME" -ForegroundColor White
        Write-Host "   Username: $DB_USER" -ForegroundColor White
        Write-Host "   Password: $DB_PASS" -ForegroundColor White
        Write-Host "   Host: localhost" -ForegroundColor White
        Write-Host "   Port: 3306" -ForegroundColor White
        Write-Host ""
        Write-Host "🔗 Connection URL:" -ForegroundColor Cyan
        Write-Host "   mysql+pymysql://$DB_USER`:$DB_PASS@localhost:3306/$DB_NAME" -ForegroundColor White
        Write-Host ""
        Write-Host "📝 Next steps:" -ForegroundColor Yellow
        Write-Host "   1. Test connection: python test-database.py" -ForegroundColor White
        Write-Host "   2. Start backend: cd backend && uvicorn main:app --reload" -ForegroundColor White
        Write-Host "   3. Start frontend: cd frontend && npm run dev" -ForegroundColor White
    } else {
        throw "MySQL command failed"
    }
    
} catch {
    Write-Host "❌ Database setup failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Troubleshooting:" -ForegroundColor Yellow
    Write-Host "   1. Make sure MySQL service is running" -ForegroundColor White
    Write-Host "   2. Check root password: $DB_ROOT_PASS" -ForegroundColor White
    Write-Host "   3. Try Docker instead: docker-compose up -d mysql" -ForegroundColor White
    exit 1
} finally {
    # Clean up temporary file
    if (Test-Path $tempFile) {
        Remove-Item $tempFile -Force
    }
}
