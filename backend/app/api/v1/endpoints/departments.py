from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ....core.database import get_db
from ....models.department import Department

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_departments(db: Session = Depends(get_db)):
    """Get all departments."""
    departments = db.query(Department).all()
    return [
        {
            "id": dept.id,
            "name": dept.name,
            "faculty": dept.faculty,
            "head_of_department": dept.head_of_department,
            "created_at": dept.created_at.isoformat() if dept.created_at else None
        }
        for dept in departments
    ]
