@echo off
echo 🚀 Setting up Academic Repository System Database...

set DB_NAME=academic_repo_db
set DB_USER=academic_user
set DB_PASS=260307
set DB_ROOT_PASS=260307

echo 📋 Creating database and user...

echo CREATE DATABASE IF NOT EXISTS %DB_NAME% CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; > temp_setup.sql
echo USE %DB_NAME%; >> temp_setup.sql
echo CREATE USER IF NOT EXISTS '%DB_USER%'@'localhost' IDENTIFIED BY '%DB_PASS%'; >> temp_setup.sql
echo CREATE USER IF NOT EXISTS '%DB_USER%'@'%%' IDENTIFIED BY '%DB_PASS%'; >> temp_setup.sql
echo GRANT ALL PRIVILEGES ON %DB_NAME%.* TO '%DB_USER%'@'localhost'; >> temp_setup.sql
echo GRANT ALL PRIVILEGES ON %DB_NAME%.* TO '%DB_USER%'@'%%'; >> temp_setup.sql
echo FLUSH PRIVILEGES; >> temp_setup.sql

echo 🔐 Executing database setup...
mysql -u root -p%DB_ROOT_PASS% < temp_setup.sql

if %errorlevel% equ 0 (
    echo ✅ Database setup completed successfully!
    echo.
    echo 📊 Database Information:
    echo    Database: %DB_NAME%
    echo    Username: %DB_USER%
    echo    Password: %DB_PASS%
    echo    Host: localhost
    echo    Port: 3306
    echo.
    echo 🔗 Connection URL:
    echo    mysql+pymysql://%DB_USER%:%DB_PASS%@localhost:3306/%DB_NAME%
    echo.
    echo 📝 Next steps:
    echo    1. Test connection: python test-database.py
    echo    2. Start backend: cd backend ^&^& uvicorn main:app --reload
    echo    3. Start frontend: cd frontend ^&^& npm run dev
) else (
    echo ❌ Database setup failed!
    echo 🔧 Try using Docker instead: docker-compose up -d mysql
)

del temp_setup.sql 2>nul
pause
