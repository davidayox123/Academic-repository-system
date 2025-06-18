<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Academic Repository System - Copilot Instructions

## Project Overview
This is a comprehensive Academic Repository System built with React TypeScript frontend and FastAPI Python backend. The system manages academic research documents with role-based access control, review workflows, and modern UI/UX.

## Tech Stack
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Framer Motion, React Query, Zustand
- **Backend**: FastAPI, SQLAlchemy, MySQL, JWT Authentication
- **Infrastructure**: Docker, Docker Compose

## Code Style Guidelines

### Frontend (React/TypeScript)
- Use functional components with hooks
- Implement TypeScript interfaces for all props and data structures
- Follow Tailwind CSS utility-first approach
- Use Framer Motion for animations
- Implement proper error boundaries and loading states
- Use React Query for data fetching and caching
- Follow atomic design principles for components

### Backend (FastAPI/Python)
- Use async/await for all endpoints
- Implement proper error handling with HTTPException
- Use Pydantic models for request/response validation
- Follow RESTful API conventions
- Implement proper authentication and authorization
- Use SQLAlchemy ORM with proper relationships
- Add comprehensive docstrings for all functions

### Database Design
- Use UUIDs for primary keys
- Implement proper foreign key relationships
- Add timestamps (created_at, updated_at) to all tables
- Use enums for status fields
- Implement soft deletes where appropriate

## Role-Based Access Control
- **Student**: Upload documents, view own documents
- **Staff**: Same as student + department documents
- **Supervisor**: Review and approve/reject documents
- **Admin**: Full system access and user management

## UI/UX Patterns
- Use glassmorphism design with backdrop-blur
- Implement smooth transitions with Framer Motion
- Follow responsive design principles
- Use semantic HTML and proper ARIA labels
- Implement dark/light theme support
- Use toast notifications for user feedback

## Security Considerations
- Validate all inputs on both frontend and backend
- Use JWT tokens with proper expiration
- Implement CORS policies
- Sanitize file uploads
- Use HTTPS in production
- Log all sensitive operations

## Performance Best Practices
- Implement code splitting and lazy loading
- Use React.memo for expensive components
- Optimize images and assets
- Implement proper caching strategies
- Use database indexes for frequently queried fields
- Implement pagination for large datasets

## Testing Guidelines
- Write unit tests for utility functions
- Implement integration tests for API endpoints
- Use React Testing Library for component tests
- Mock external dependencies
- Test error scenarios and edge cases

## Development Workflow
- Use feature branches for new functionality
- Write meaningful commit messages
- Update documentation for API changes
- Run linting and formatting before commits
- Test thoroughly before merging

When generating code, please follow these patterns and conventions to maintain consistency across the project.
