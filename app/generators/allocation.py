import os
import uuid
import random
from datetime import date, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.models.project import Project
from app.models.employee import Employee
from app.models.project_allocation import ProjectAllocation, ProjectRole
from app.schemas.project_allocation import ProjectAllocationCreate
from fastapi import HTTPException

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionCustom = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_roles():
    return [role for role in ProjectRole]

def get_status_options():
    from app.models.project_allocation_status_log import AllocationStatus
    return [status for status in AllocationStatus]

def create_project_allocation(db: Session, allocation_data: ProjectAllocationCreate):
    allocation = ProjectAllocation(**allocation_data.model_dump())
    db.add(allocation)
    db.commit()
    db.refresh(allocation)
    return allocation

def generate_allocations(n):
    db: Session = SessionCustom()
    employees = db.query(Employee).all()
    projects = db.query(Project).all()
    roles = get_roles()
    status_options = get_status_options()

    for _ in range(n):
        employee = random.choice(employees)
        project = random.choice(projects)

        # Check if project has reached max team size
        current_allocs = db.query(ProjectAllocation).filter(ProjectAllocation.project_id == project.id).count()
        if current_allocs >= project.max_team_size:
            print(f"Skipping allocation for {employee.name} in project {project.name} - max team size reached.")
            continue

        allocation_data = ProjectAllocationCreate(
            project_id=project.id,
            employee_id=employee.id,
            role=random.choice([role.name for role in roles]),
            status=random.choice([status.name for status in status_options]),
            allocated_on=date.today() - timedelta(days=random.randint(1, 10)),
            deadline=date.today() + timedelta(days=random.randint(7, 30)),
        )
        
        allocation = create_project_allocation(db, allocation_data)
        print(f"Created allocation for {employee.name} in project {project.name} with status {allocation.status.name}.")

    db.close()

if __name__ == "__main__":
    n = int(input("Enter the number of allocations to generate: "))
    generate_allocations(n)