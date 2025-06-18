#!/bin/bash

# Academic Repository System Setup Script
echo "🎓 Setting up Academic Repository System..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create uploads directory
echo "📁 Creating uploads directory..."
mkdir -p uploads

# Copy environment file
echo "⚙️ Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from .env.example"
    echo "⚠️  Please update the .env file with your configuration"
else
    echo "✅ .env file already exists"
fi

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Install backend dependencies (if running without Docker)
echo "🐍 Setting up Python backend..."
cd backend
if command -v python3 &> /dev/null; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo "✅ Backend dependencies installed"
else
    echo "⚠️  Python3 not found. Backend will run in Docker container."
fi
cd ..

# Start the services
echo "🚀 Starting services with Docker Compose..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "🎉 Academic Repository System is now running!"
echo ""
echo "📍 Access points:"
echo "   - Frontend: http://localhost:5173"
echo "   - Backend API: http://localhost:8000"
echo "   - API Documentation: http://localhost:8000/docs"
echo "   - MySQL: localhost:3306"
echo ""
echo "👥 Default login credentials:"
echo "   - Admin: admin@university.edu / password123"
echo "   - Supervisor: supervisor@university.edu / password123"  
echo "   - Student: student@university.edu / password123"
echo ""
echo "⚠️  Remember to change default passwords in production!"
echo ""
echo "🛠️  To stop the services: docker-compose down"
echo "🔧  To view logs: docker-compose logs -f"
