from uuid import UUID
from sqlalchemy.orm import Session
from app.models.project_allocation import ProjectAllocation
from app.schemas.project_allocation import ProjectAllocationCreate
from app.models.project_allocation import AllocationStatus

def create_project_allocation(db: Session, allocation_data: ProjectAllocationCreate):
    """Assign an employee to a project"""
    allocation = ProjectAllocation(**allocation_data.model_dump())
    db.add(allocation)
    db.commit()
    db.refresh(allocation)
    return allocation

def get_project_allocations(db: Session, project_id: UUID):
    """Get all allocations for a specific project"""
    return db.query(ProjectAllocation).filter(ProjectAllocation.project_id == project_id).all()

def update_project_allocation_status(db: Session, allocation_id: UUID, status: AllocationStatus):
    """Update allocation status (active, completed, removed)"""
    allocation = db.query(ProjectAllocation).filter(ProjectAllocation.id == allocation_id).first()
    if allocation:
        allocation.status = status
        db.commit()
        db.refresh(allocation)
    return allocation

def remove_employee_from_project(db: Session, allocation_id: UUID):
    """Remove an employee from a project"""
    allocation = db.query(ProjectAllocation).filter(ProjectAllocation.id == allocation_id).first()
    if allocation:
        db.delete(allocation)
        db.commit()
    return allocation
