import os
import random
from dotenv import load_dotenv
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.models.project_allocation import ProjectAllocation
from app.models.project_allocation_status_log import AllocationStatus, ProjectAllocationStatusLog
from app.crud.project_allocation import update_project_allocation_status

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionCustom = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def log_update_allocation_status(db: Session, allocation_id, new_status):
    allocation = db.query(ProjectAllocation).filter(ProjectAllocation.id == allocation_id).first()
    if not allocation or allocation.status == new_status:
        return

    # Random duration between 1 hour and 3 days
    duration = timedelta(seconds=random.randint(3600, 3 * 24 * 3600))
    fake_changed_at = allocation.updated_at + duration if allocation.updated_at else datetime.utcnow()

    # Log the status change
    log = ProjectAllocationStatusLog(
        allocation_id=allocation.id,
        from_status=allocation.status,
        to_status=new_status,
        changed_at=fake_changed_at,
        duration_spent=duration
    )
    db.add(log)
    allocation.status = new_status
    allocation.updated_at = fake_changed_at
    db.commit()
    db.refresh(allocation)

def generate_status_logs():
    db: Session = SessionCustom()
    allocations = db.query(ProjectAllocation).all()
    statuses = [status.name for status in AllocationStatus]

    for alloc in allocations:
        num_changes = random.randint(2, 5)  # Simulate between 2 and 5 status changes for each allocation
        current_status = alloc.status

        for _ in range(num_changes):
            # Pick a new status, ensuring it's different from the current status
            new_status = random.choice([s for s in statuses if s != current_status])

            # Apply the status change and log it
            log_update_allocation_status(db, alloc.id, new_status)
            update_project_allocation_status(db, alloc.id, new_status)

            print(f"Updated status for allocation {alloc.id} from {current_status} to {new_status}")

            # Update current status for the next iteration
            current_status = new_status

    db.close()

if __name__ == "__main__":
    generate_status_logs()