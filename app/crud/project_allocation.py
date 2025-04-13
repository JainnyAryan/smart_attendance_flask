from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.api.performance import get_all_employee_scores
from app.models.project_allocation import ProjectAllocation, AllocationStatus
from app.schemas.project_allocation import ProjectAllocationCreate, ProjectAllocationResponse
from app.models.employee import Employee
from app.models.project import Project


def create_project_allocation(db: Session, allocation_data: ProjectAllocationCreate):
    """Assign an employee to a project and return full project and employee details."""
    # Check how many employees are already allocated to this project
    current_allocs = db.query(ProjectAllocation).filter(
        ProjectAllocation.project_id == allocation_data.project_id
    ).count()
    # Fetch project details to get max_team_size
    project = db.query(Project).filter_by(
        id=allocation_data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_allocs >= project.max_team_size:
        raise HTTPException(
            status_code=400, detail="Project has reached its max team size")
    # Proceed with creating the allocation
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
        .order_by(ProjectAllocation.created_at.desc())
        .filter(ProjectAllocation.project_id == project_id)
        .all()
    )


def get_allocations_by_employee_id(db: Session, employee_id: UUID):
    """Get all allocations for a specific employee, including project and employee details."""
    return (
        db.query(ProjectAllocation)
        .options(joinedload(ProjectAllocation.project), joinedload(ProjectAllocation.employee))
        .order_by(ProjectAllocation.created_at.desc())
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
    """Suggest employees based on skill match, experience, and score."""
    required_skills = set(project.required_skills)
    min_experience = project.min_experience

    # Step 1: Get all employees with their allocation count and skills
    employees = db.query(
        Employee.id,
        Employee.experience,
        func.count(ProjectAllocation.id).label("allocation_count"),
        Employee.skills
    ).outerjoin(ProjectAllocation, Employee.id == ProjectAllocation.employee_id) \
     .group_by(Employee.id) \
     .all()

    # Step 2: Get employee scores and convert to dictionary
    employee_scores = get_all_employee_scores(db)
    employee_scores_dict = {
        emp['employee_id']: emp['score'] for emp in employee_scores
    }

    # Step 3: Prepare employee data
    employee_data = []
    for emp_id, experience, allocation_count, emp_skills in employees:
        emp_skills = set(emp_skills) if emp_skills else set()
        match_count = len(required_skills.intersection(emp_skills))
        score = employee_scores_dict.get(emp_id, 0.0)

        if match_count > 0 and experience >= min_experience and allocation_count < 4:
            employee_data.append({
                "employee_id": emp_id,
                "experience": experience,
                "skills": emp_skills,
                "allocation_count": allocation_count,
                "match_count": match_count,
                "score": score
            })

    # Step 4: Sort by match_count, then experience, then score (all descending)
    employee_data.sort(
        key=lambda x: (-x["match_count"], -x["experience"], -x["score"])
    )

    # Step 5: Greedy selection to maximize skill coverage
    selected_employees = []
    covered_skills = set()

    for emp in employee_data:
        new_skills = emp["skills"] - covered_skills
        if new_skills:
            selected_employees.append(emp)
            covered_skills.update(new_skills)
        if covered_skills >= required_skills:
            break

    return selected_employees


def get_allocation_statuses(db: Session = None):
    return [status.value for status in AllocationStatus]
