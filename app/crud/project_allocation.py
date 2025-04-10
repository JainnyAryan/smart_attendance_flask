from uuid import UUID
from sqlalchemy import func
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
    allocation = db.query(ProjectAllocation).filter(
        ProjectAllocation.id == allocation_id).first()
    if allocation:
        allocation.status = status
        db.commit()
        db.refresh(allocation)
        return get_project_allocation_by_id(db, allocation_id)
    return None


def remove_employee_from_project(db: Session, allocation_id: UUID):
    """Remove an employee from a project and return the deleted allocation details."""
    allocation = db.query(ProjectAllocation).filter(
        ProjectAllocation.id == allocation_id).first()
    if allocation:
        db.delete(allocation)
        db.commit()
        return allocation
    return None


def suggested_employees(db: Session, project: Project):
    """Get all suggested employees for the project based on required skills and experience."""
    required_skills = set(project.required_skills)
    min_experience = project.min_experience

    # Fetch all employees along with their skills and allocation count
    employees = db.query(
        Employee.id,
        Employee.experience,
        func.count(ProjectAllocation.id).label("allocation_count"),
        Employee.skills
    ).outerjoin(ProjectAllocation, Employee.id == ProjectAllocation.employee_id) \
     .group_by(Employee.id) \
     .all()

    # Step 1: Prepare employee data
    employee_data = []
    for emp_id, experience, allocation_count, emp_skills in employees:
        emp_skills = set(emp_skills) if emp_skills else set()
        matching_skills = required_skills.intersection(emp_skills)
        match_count = len(matching_skills)

        # Store only eligible employees (matching at least one skill and meeting experience criteria)
        if match_count > 0 and experience >= min_experience and allocation_count < 4:
            employee_data.append(
                (emp_id, experience, emp_skills, allocation_count))

    # Step 2: Sort employees by number of skills matched (descending) and experience (descending)
    employee_data.sort(
        key=lambda x: (-len(x[2].intersection(required_skills)), -x[1]))

    # Step 3: Greedy selection to maximize skill coverage
    selected_employees = []
    covered_skills = set()

    for emp_id, experience, emp_skills, allocation_count in employee_data:
        # Check if adding this employee helps cover more required skills
        new_skills = emp_skills - covered_skills  # Skills this employee contributes
        if new_skills:
            selected_employees.append((emp_id, experience))
            covered_skills.update(new_skills)

        # Stop if all required skills are covered
        if covered_skills >= required_skills:
            break

    # Step 4: Sort final selected employees by experience (descending)
    selected_employees.sort(key=lambda x: -x[1])
    return selected_employees
