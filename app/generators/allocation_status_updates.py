import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.models.project_allocation import ProjectAllocation
from app.models.project_allocation_status_log import AllocationStatus, ProjectAllocationStatusLog
from app.crud.project_allocation import update_project_allocation_status
import random

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionCustom = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def log_status(db, alloc, from_status, to_status, changed_at, duration):
    log = ProjectAllocationStatusLog(
        allocation_id=alloc.id,
        from_status=from_status,
        to_status=to_status,
        changed_at=changed_at,
        duration_spent=duration
    )
    db.add(log)
    alloc.status = to_status
    alloc.updated_at = changed_at
    db.commit()
    db.refresh(alloc)

def generate_realistic_status_logs():
    db: Session = SessionCustom()
    allocations = db.query(ProjectAllocation).all()

    for alloc in allocations:
        current_status = AllocationStatus.PENDING
        start_time = alloc.allocated_on or (datetime.utcnow() - timedelta(days=10))
        log_time = datetime.combine(start_time, datetime.min.time())
        print(f"\nAllocation: {alloc.id} - Starting at {log_time.date()}")

        # Step 1: PENDING to ACTIVE
        duration = timedelta(hours=random.randint(2, 10))
        log_time += duration
        log_status(db, alloc, current_status, AllocationStatus.ACTIVE, log_time, duration)
        print(f"  {current_status.name} → ACTIVE for {duration}")
        current_status = AllocationStatus.ACTIVE

        # Step 2: Optional ON_HOLD + return to ACTIVE
        if random.random() < 0.5:  # 50% chance to go on hold
            duration = timedelta(hours=random.randint(1, 8))
            log_time += duration
            log_status(db, alloc, current_status, AllocationStatus.ON_HOLD, log_time, duration)
            print(f"  ACTIVE → ON_HOLD for {duration}")
            current_status = AllocationStatus.ON_HOLD

            duration = timedelta(hours=random.randint(2, 12))
            log_time += duration
            log_status(db, alloc, current_status, AllocationStatus.ACTIVE, log_time, duration)
            print(f"  ON_HOLD → ACTIVE for {duration}")
            current_status = AllocationStatus.ACTIVE

        # Step 3: End with COMPLETED or REMOVED
        final_status = random.choice([AllocationStatus.COMPLETED, AllocationStatus.REMOVED])
        duration = timedelta(hours=random.randint(1, 6))
        log_time += duration
        log_status(db, alloc, current_status, final_status, log_time, duration)
        print(f"  {current_status.name} → {final_status.name} for {duration}")

    db.close()

if __name__ == "__main__":
    generate_realistic_status_logs()