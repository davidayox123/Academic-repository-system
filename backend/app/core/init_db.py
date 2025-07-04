"""
Database initialization script with sample data
"""
import asyncio
from sqlalchemy.orm import Session
from .database import engine, get_sync_db
from ..models import *
import uuid
from datetime import datetime, timedelta
import random

async def create_sample_departments():
    """Create sample departments"""
    departments = [
        {
            "name": "Computer Science",
            "code": "CS",
            "faculty": "Engineering & Technology",
            "description": "Department of Computer Science and Information Technology",
            "head_of_department": "Dr. John Smith",
            "contact_email": "cs@university.edu",
            "building": "Engineering Building",
            "room_number": "E-201"
        },
        {
            "name": "Mathematics",
            "code": "MATH",
            "faculty": "Science",
            "description": "Department of Pure and Applied Mathematics",
            "head_of_department": "Prof. Sarah Johnson",
            "contact_email": "math@university.edu",
            "building": "Science Building",
            "room_number": "S-301"
        },
        {
            "name": "Physics",
            "code": "PHYS",
            "faculty": "Science",
            "description": "Department of Physics and Astronomy",
            "head_of_department": "Dr. Michael Brown",
            "contact_email": "physics@university.edu",
            "building": "Science Building",
            "room_number": "S-201"
        },
        {
            "name": "Business Administration",
            "code": "BUS",
            "faculty": "Business",
            "description": "Department of Business Administration and Management",
            "head_of_department": "Prof. Lisa Anderson",
            "contact_email": "business@university.edu",
            "building": "Business Building",
            "room_number": "B-101"
        }
    ]
    
    return [Department(**dept) for dept in departments]

async def create_sample_users(departments):
    """Create sample users for each role"""
    users = []
    
    # Admin users
    admin_user = User(
        email="admin@university.edu",
        name="System Administrator",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewjyJo6oK8F9mKFy",  # password: admin123
        role=UserRole.ADMIN,
        department_id=departments[0].id
    )
    users.append(admin_user)
    
    # Supervisors
    supervisors = [
        User(
            email="supervisor1@university.edu",
            name="Dr. Alice Johnson",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewjyJo6oK8F9mKFy",
            role=UserRole.SUPERVISOR,
            department_id=departments[0].id
        ),
        User(
            email="supervisor2@university.edu",
            name="Prof. Robert Wilson",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewjyJo6oK8F9mKFy",
            role=UserRole.SUPERVISOR,
            department_id=departments[1].id
        )
    ]
    users.extend(supervisors)
    
    # Staff members
    staff = [
        User(
            email="staff1@university.edu",
            name="Jane Smith",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewjyJo6oK8F9mKFy",
            role=UserRole.STAFF,
            department_id=departments[0].id
        ),
        User(
            email="staff2@university.edu",
            name="Mark Davis",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewjyJo6oK8F9mKFy",
            role=UserRole.STAFF,
            department_id=departments[1].id
        ),
        User(
            email="staff3@university.edu",
            name="Emily Chen",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewjyJo6oK8F9mKFy",
            role=UserRole.STAFF,
            department_id=departments[2].id
        )
    ]
    users.extend(staff)
    
    # Students
    students = [
        User(
            email="student1@university.edu",
            name="Alex Thompson",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewjyJo6oK8F9mKFy",
            role=UserRole.STUDENT,
            department_id=departments[0].id
        ),
        User(
            email="student2@university.edu",
            name="Maria Garcia",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewjyJo6oK8F9mKFy",
            role=UserRole.STUDENT,
            department_id=departments[0].id
        ),
        User(
            email="student3@university.edu",
            name="David Lee",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewjyJo6oK8F9mKFy",
            role=UserRole.STUDENT,
            department_id=departments[1].id
        ),
        User(
            email="student4@university.edu",
            name="Sarah Miller",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewjyJo6oK8F9mKFy",
            role=UserRole.STUDENT,
            department_id=departments[2].id
        )
    ]
    users.extend(students)
    
    return users

async def create_sample_documents(users, departments):
    """Create sample documents"""
    documents = []
    students = [u for u in users if u.role == UserRole.STUDENT]
    supervisors = [u for u in users if u.role == UserRole.SUPERVISOR]
    
    doc_titles = [
        "Machine Learning Applications in Healthcare",
        "Quantum Computing Research Paper",
        "Data Structures and Algorithms Analysis",
        "Web Development Best Practices",
        "Artificial Intelligence Ethics",
        "Database Design Principles",
        "Software Engineering Methodologies",
        "Computer Networks Security"
    ]
    
    statuses = [DocumentStatus.SUBMITTED, DocumentStatus.APPROVED, DocumentStatus.UNDER_REVIEW, DocumentStatus.REJECTED]
    
    for i, title in enumerate(doc_titles):
        student = random.choice(students)
        supervisor = random.choice(supervisors)
        
        doc = Document(
            title=title,
            status=random.choice(statuses),
            uploader_id=student.id,
            department_id=student.department_id,
            supervisor_id=supervisor.id,
            upload_date=datetime.now() - timedelta(days=random.randint(1, 30)),
        )
        documents.append(doc)
    return documents

async def init_database():
    """Initialize database with sample data"""
    session = get_sync_db()
    try:
        # Check if data already exists
        if session.query(Department).first():
            print("✅ Database already has sample data")
            return
            
        # Create departments
        departments = await create_sample_departments()
        session.add_all(departments)
        session.flush()  # Get IDs
        
        # Create users
        users = await create_sample_users(departments)
        session.add_all(users)
        session.flush()  # Get IDs
        # Create documents
        documents = await create_sample_documents(users, departments)
        session.add_all(documents)
        session.flush()  # Get IDs
        
        # Update department statistics
        for dept in departments:
            dept.total_users = len([u for u in users if u.department_id == dept.id])
            dept.total_documents = len([d for d in documents if d.department_id == dept.id])
        
        session.commit()
        print("✅ Database initialized successfully with sample data!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error initializing database: {e}")
        raise
    finally:
        session.close()

# Alias for backwards compatibility
init_sample_data = init_database

if __name__ == "__main__":
    asyncio.run(init_database())
