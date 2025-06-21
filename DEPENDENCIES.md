# Academic Repository System - Dependencies

This document lists all the dependencies required for the Academic Repository System, both for the backend (Python/FastAPI) and frontend (React/TypeScript).

## Backend Dependencies (Python)

### Core Framework & API
- **fastapi==0.115.6** - Modern web framework for building APIs
- **uvicorn[standard]==0.32.1** - ASGI server for FastAPI
- **python-multipart==0.0.19** - Support for multipart form data (file uploads)

### Database & ORM
- **sqlalchemy==2.0.25** - SQL toolkit and Object-Relational Mapping
- **mysql-connector-python==9.1.0** - MySQL database connector
- **pymysql==1.1.1** - Pure Python MySQL client
- **alembic==1.14.0** - Database migration tool

### Authentication & Security
- **python-jose[cryptography]==3.3.0** - JWT token handling
- **passlib[bcrypt]==1.7.4** - Password hashing
- **bcrypt==4.2.1** - Password hashing algorithm
- **PyJWT==2.10.1** - JSON Web Token implementation
- **cryptography==44.0.0** - Cryptographic recipes and primitives

### Data Validation & Configuration
- **pydantic==2.9.0** - Data validation using Python type annotations
- **pydantic-settings==2.5.2** - Settings management
- **email-validator==2.2.0** - Email address validation
- **python-decouple==3.8** - Configuration management
- **python-dotenv==1.0.1** - Environment variable loading

### File Processing
- **Pillow==10.1.0** - Image processing library (thumbnails, image handling)
- **PyMuPDF==1.23.8** - PDF processing library (previews, text extraction)
- **python-magic==0.4.27** - File type detection by content
- **python-docx==1.1.0** - Microsoft Word document processing
- **aiofiles==24.1.0** - Asynchronous file operations

### Real-time & Enhanced Features
- **websockets==12.0** - WebSocket support for real-time updates
- **python-dateutil==2.8.2** - Advanced date/time parsing and manipulation

## Frontend Dependencies (React/TypeScript)

### Core Framework
- **react==^18.2.0** - React library
- **react-dom==^18.2.0** - React DOM rendering
- **typescript==^4.9.3** - TypeScript compiler
- **vite==^4.1.0** - Build tool and dev server

### Routing & Navigation
- **react-router-dom==^6.30.1** - Client-side routing

### State Management & Data Fetching
- **zustand==^4.5.7** - Lightweight state management
- **@tanstack/react-query==^5.81.0** - Data fetching and caching
- **axios==^1.10.0** - HTTP client for API calls

### UI & Styling
- **tailwindcss==^3.2.7** - Utility-first CSS framework
- **framer-motion==^10.18.0** - Animation library
- **lucide-react==^0.321.0** - Icon library
- **clsx==^1.2.1** - Conditional CSS class utility
- **tailwind-merge==^1.10.0** - Merge Tailwind CSS classes

### Forms & User Input
- **react-hook-form==^7.43.5** - Form handling library
- **@hookform/resolvers==^2.9.11** - Form validation resolvers
- **zod==^3.20.6** - Schema validation
- **react-dropzone==^14.3.8** - File upload component

### User Experience
- **react-hot-toast==^2.5.2** - Toast notifications
- **date-fns==^2.29.3** - Date utility library

### Development Tools
- **@vitejs/plugin-react==^3.1.0** - Vite React plugin
- **eslint==^8.35.0** - Code linting
- **@typescript-eslint/eslint-plugin==^5.54.0** - TypeScript ESLint rules
- **@typescript-eslint/parser==^5.54.0** - TypeScript ESLint parser
- **autoprefixer==^10.4.14** - CSS autoprefixer
- **postcss==^8.4.21** - CSS post-processor

## Installation Instructions

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

### Docker Setup (Recommended)
```bash
docker-compose up -d
```

## Key Features Enabled by Dependencies

### File Processing Capabilities
- **Image thumbnails** - Pillow for image processing
- **PDF previews** - PyMuPDF for PDF rendering
- **Document type detection** - python-magic for MIME type detection
- **Word document processing** - python-docx for .docx files

### Real-time Features
- **Live notifications** - WebSockets for real-time updates
- **Activity feeds** - Real-time activity logging and broadcasting

### Security Features
- **Password hashing** - bcrypt for secure password storage
- **JWT authentication** - python-jose for token management
- **File type validation** - python-magic for security validation

### Advanced Database Features
- **Relationship mapping** - SQLAlchemy ORM for complex queries
- **Migration support** - Alembic for database versioning
- **Connection pooling** - Built-in MySQL connector features

### Modern UI/UX
- **Responsive design** - Tailwind CSS utility classes
- **Smooth animations** - Framer Motion for transitions
- **Form validation** - React Hook Form with Zod schemas
- **Data caching** - React Query for optimized API calls

All dependencies are carefully selected to provide a robust, secure, and feature-rich academic repository system with modern development practices and excellent user experience.
