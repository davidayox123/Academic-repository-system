# Academic Repository System 🎓

A modern, sleek, and interactive web application for managing academic research outputs with role-based access control, document workflow management, and stunning UI/UX.

## 🚀 Features

- **Modern UI/UX**: Sleek animations, interactive components, dark/light theme
- **Role-Based Access**: Student, Staff, Supervisor, Admin roles
- **Document Management**: Upload, review, approve/reject workflow
- **Advanced Search**: Full-text search with filtering
- **Audit Trail**: Complete action logging
- **Responsive Design**: Works on all devices
- **Real-time Updates**: Live notifications and updates

## 🛠️ Tech Stack

### Frontend
- React 18 + TypeScript
- Vite (Build tool)
- Tailwind CSS (Styling)
- Framer Motion (Animations)
- React Query (Data fetching)
- Zustand (State management)
- React Hook Form (Forms)
- Lucide React (Icons)

### Backend
- FastAPI (Python)
- SQLAlchemy (ORM)
- MySQL (Database)
- JWT Authentication
- File upload handling
- Background tasks

## 🏃‍♂️ Quick Start

### Option 1: Using Docker (Recommended)

1. **Prerequisites**:
   - Docker Desktop
   - Git

2. **Clone and Run**:
   ```bash
   git clone <your-repo-url>
   cd Academic-repository-system
   
   # Windows
   setup.bat
   
   # macOS/Linux
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Access the Application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. **Install Python 3.11+**
2. **Setup Virtual Environment**:
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Database**:
   - Install MySQL 8.0+
   - Create database `academic_repo_db`
   - Update connection string in `.env`

5. **Run Backend**:
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend Setup

1. **Install Node.js 18+**
2. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

3. **Start Development Server**:
   ```bash
   npm run dev
   ```

## 👤 Default Users

After setup, you can login with these default accounts:

- **Admin**: admin@university.edu / password123
- **Supervisor**: supervisor@university.edu / password123
- **Student**: student@university.edu / password123

⚠️ **Remember to change default passwords in production!**

## 📁 Project Structure

```
Academic-repository-system/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Application pages
│   │   ├── contexts/       # React contexts
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   ├── utils/          # Utility functions
│   │   └── styles/         # CSS and styling
│   ├── public/             # Static assets
│   └── package.json
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── uploads/            # File storage
│   └── requirements.txt
├── database/               # Database scripts
├── docker-compose.yml      # Docker setup
└── README.md
```

## 🎨 UI Features

- **Smooth Animations**: Framer Motion powered transitions
- **Glassmorphism Design**: Modern translucent effects
- **Dark/Light Theme**: Automatic and manual theme switching
- **Responsive Layout**: Mobile-first responsive design
- **Interactive Components**: Hover effects and micro-interactions
- **Loading States**: Beautiful loading skeletons
- **Toast Notifications**: Real-time feedback system
- **Drag & Drop**: Intuitive file upload interface

## 🔧 Development

### Frontend Development

```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
```

### Backend Development

```bash
cd backend
uvicorn main:app --reload    # Start development server
python -m pytest            # Run tests
alembic upgrade head         # Run database migrations
```

### Database Management

```bash
# Create new migration
cd backend
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild services
docker-compose up --build

# Execute commands in containers
docker-compose exec backend python manage.py shell
docker-compose exec frontend sh
```

## 🌟 Key Features Breakdown

### 1. Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- Password strength validation
- Session management

### 2. Document Management
- File upload with validation
- Multiple file format support
- Metadata extraction
- Version control
- Bulk operations

### 3. Review Workflow
- Supervisor approval process
- Comment system
- Status tracking
- Email notifications
- Deadline management

### 4. Search & Discovery
- Full-text search
- Advanced filtering
- Category browsing
- Recent documents
- Popular content

### 5. Analytics & Reporting
- Dashboard metrics
- Download statistics
- User activity tracking
- Department analytics
- Export capabilities

### 6. Security Features
- Input validation
- SQL injection prevention
- XSS protection
- File type validation
- Audit logging

## 🚀 Deployment

### Production Environment

1. **Environment Variables**:
   ```bash
   # Copy and configure
   cp .env.example .env
   ```

2. **Security Checklist**:
   - [ ] Change default passwords
   - [ ] Update SECRET_KEY
   - [ ] Configure HTTPS
   - [ ] Set up firewall rules
   - [ ] Enable database backups
   - [ ] Configure monitoring

3. **Docker Deployment**:
   ```bash
   # Production build
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Cloud Deployment Options

- **AWS**: EC2 + RDS + S3
- **Google Cloud**: Compute Engine + Cloud SQL + Cloud Storage
- **Azure**: Virtual Machines + Azure Database + Blob Storage
- **DigitalOcean**: Droplets + Managed Database + Spaces

## 🧪 Testing

```bash
# Frontend tests
cd frontend
npm run test

# Backend tests
cd backend
pytest

# E2E tests
npm run test:e2e
```

## 📈 Performance Optimization

- **Frontend**: Code splitting, lazy loading, image optimization
- **Backend**: Database indexing, query optimization, caching
- **Infrastructure**: CDN, load balancing, auto-scaling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: [Wiki](link-to-wiki)
- **Issues**: [GitHub Issues](link-to-issues)
- **Email**: support@example.com
- **Discord**: [Community Server](link-to-discord)

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] AI-powered document categorization
- [ ] Integration with external plagiarism tools
- [ ] Real-time collaboration features
- [ ] Advanced workflow automation

---

Built with ❤️ for modern academic institutions

**Made by**: [Your Name]
**Version**: 1.0.0
**Last Updated**: June 2025
    ...reactDom.configs.recommended.rules,
  },
})
```
