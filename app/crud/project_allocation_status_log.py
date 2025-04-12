from datetime import datetime
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.project_allocation import ProjectAllocation
from app.models.project_allocation_status_log import ProjectAllocationStatusLog


def get_status_logs_by_allocation_id(db: Session, allocation_id: UUID):
    """Return all status logs for a specific allocation, sorted by changed_at."""
    return (
        db.query(ProjectAllocationStatusLog)
        .filter(ProjectAllocationStatusLog.allocation_id == allocation_id)
        .order_by(ProjectAllocationStatusLog.changed_at)
        .all()
    )


def log_update_allocation_status(db: Session, allocation_id: UUID, new_status: str):
    allocation = db.query(ProjectAllocation).filter(
        ProjectAllocation.id == allocation_id).first()

    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    if allocation.status != new_status:
        log = ProjectAllocationStatusLog(
            allocation_id=allocation.id,
            from_status=allocation.status,
            to_status=new_status,
            changed_at=datetime.utcnow(),
            # assuming updated_at is being tracked
            duration_spent=datetime.utcnow() - allocation.updated_at
        )
        db.add(log)
        allocation.status = new_status
        db.commit()
        db.refresh(allocation)

    return allocation
