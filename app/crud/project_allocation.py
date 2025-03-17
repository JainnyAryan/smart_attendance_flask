from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.models.project_allocation import ProjectAllocation, AllocationStatus
from app.schemas.project_allocation import ProjectAllocationCreate, ProjectAllocationResponse
from app.models.employee import Employee
from app.models.project import Project

def create_project_allocation(db: Session, allocation_data: ProjectAllocationCreate):
    """Assign an employee to a project and return full project and employee details."""
    allocation = ProjectAllocation(**allocation_data.model_dump())
    db.add(allocation)
    db.commit()
    db.refresh(allocation)

    return get_project_allocation_by_id(db, allocation.id)


def get_project_allocations(db: Session, project_id: UUID):
    """Get all allocations for a specific project, including employee and project details."""
    return (
        db.query(ProjectAllocation)
        .options(joinedload(ProjectAllocation.employee), joinedload(ProjectAllocation.project))
        .filter(ProjectAllocation.project_id == project_id)
        .all()
    )


def get_allocations_by_employee_id(db: Session, employee_id: UUID):
    """Get all allocations for a specific employee, including project and employee details."""
    return (
        db.query(ProjectAllocation)
        .options(joinedload(ProjectAllocation.project), joinedload(ProjectAllocation.employee))
        .filter(ProjectAllocation.employee_id == employee_id)
        .all()
    )


def get_project_allocation_by_id(db: Session, allocation_id: UUID):
    """Get a single project allocation by ID, including project and employee details."""
    return (
        db.query(ProjectAllocation)
        .options(joinedload(ProjectAllocation.project), joinedload(ProjectAllocation.employee))
        .filter(ProjectAllocation.id == allocation_id)
        .first()
    )


def update_project_allocation_status(db: Session, allocation_id: UUID, status: AllocationStatus):
    """Update allocation status (active, completed, removed) and return full details."""
    allocation = db.query(ProjectAllocation).filter(ProjectAllocation.id == allocation_id).first()
    if allocation:
        allocation.status = status
        db.commit()
        db.refresh(allocation)
        return get_project_allocation_by_id(db, allocation_id)
    return None


def remove_employee_from_project(db: Session, allocation_id: UUID):
    """Remove an employee from a project and return the deleted allocation details."""
    allocation = db.query(ProjectAllocation).filter(ProjectAllocation.id == allocation_id).first()
    if allocation:
        db.delete(allocation)
        db.commit()
        return allocation
    return None