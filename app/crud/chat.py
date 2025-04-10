from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from app.crud.attendance import get_attendance_calendar_data
from app.crud.project_allocation import suggested_employees
from app.models.biometric_log import BiometricLog
from app.models.employee import Employee
from datetime import date, datetime, timedelta

from app.models.project import Project
from app.models.project_allocation import ProjectAllocation
from app.models.system_log import SystemLog
from app.models.user import User


def get_my_name(user: User):
    if user.is_admin:
        return "Admin"
    employees: list[Employee] = user.employee
    if employees:
        return employees[0].name
    return ""


def get_my_employee_today_attendance_data(db: Session, user: User):
    employees: list[Employee] = user.employee
    if not employees:
        return None
    employee = employees[0]
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())

    biometric_logs = db.query(BiometricLog).filter(
        BiometricLog.emp_id == employee.id,
        BiometricLog.in_time >= today_start,
        BiometricLog.in_time <= today_end
    ).all()

    system_logs = db.query(SystemLog).filter(
        SystemLog.emp_id == employee.id,
        SystemLog.start_time >= today_start,
        SystemLog.start_time <= today_end
    ).all()

    return {
        "biometric_logs": biometric_logs,
        "system_logs": system_logs,
    }


def get_my_project_allocations(db: Session, user: User):
    employees: list[Employee] = user.employee
    if not employees:
        return None
    employee = employees[0]
    allocations = db.query(ProjectAllocation).filter(
        ProjectAllocation.employee_id == employee.id
    ).all()
    return allocations


def get_attendance_stats(db: Session, name: str):
    res = db.query(Employee).filter(func.lower(Employee.name).ilike(name))
    emp = res.first()

    if not emp:
        return None

    end_date = datetime.today().date().strftime("%Y-%m-%d")  # Convert to string
    start_date = (datetime.today().date() - timedelta(days=30)
                  ).strftime("%Y-%m-%d")  # Convert to string

    return get_attendance_calendar_data(db=db, emp_id=emp.id, start_date=start_date, end_date=end_date)


def get_all_projects(db: Session):
    res = db.query(Project).order_by(Project.created_at.desc()).all()
    return res


def get_project_details(db: Session, code: str):
    project = db.query(Project).filter(
        or_(
            func.lower(Project.code).ilike(f"%{code.lower()}%"),
        )
    ).first()
    if not project:
        return None
    return project


def get_employee_details(db: Session, query: str):
    res = db.query(Employee).filter(
        or_(
            func.lower(Employee.name).ilike(f"%{query.lower()}%"),
            Employee.emp_code == query
        )
    )
    emp = res.first()
    return emp


def get_project_allocations_of_project(db: Session, code: str):
    project = db.query(Project).filter(
        or_(
            func.lower(Project.code).ilike(f"%{code.lower()}%"),
        )
    ).first()

    if not project:
        return None

    allocations = db.query(ProjectAllocation).filter(
        ProjectAllocation.project_id == project.id
    ).all()

    return allocations


def get_suggested_employees_for_project(db: Session, code: str):
    project = db.query(Project).filter(
        or_(
            func.lower(Project.code).ilike(f"%{code.lower()}%"),
        )
    ).first()

    if not project:
        return None

    suggestions = suggested_employees(db=db, project=project)
    ids = [emp[0] for emp in suggestions]
    employees = db.query(Employee).filter(
        Employee.id.in_(ids)
    ).all()
    return employees


def allocate_emp_to_project(db: Session, emp: str, project_code: str):
    employee = db.query(Employee).filter(or_(
        func.lower(Employee.emp_code).ilike(f"%{emp.lower()}%"),
        func.lower(Employee.name).ilike(f"%{emp.lower()}%"),
    )).first()
    project = db.query(Project).filter(
        or_(
            func.lower(Project.code).ilike(f"%{project_code.lower()}%"),
        )
    ).first()
