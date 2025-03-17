from datetime import timedelta
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.auth.auth import get_current_admin
from app.crud.analytics import calculate_time_wastage
from app.crud.attendance import get_attendance_calendar_data
from app.crud.biometric_log import *
from app.crud.employee import create_employee, get_employee, get_all_employees, update_employee, delete_employee
from app.crud.project import *
from app.crud.project_allocation import *
from app.crud.system_log import get_logs_by_emp_id, get_logs_by_emp_id_in_date_range
from app.schemas.biometric_log import *
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.crud.department import create_department, get_department, get_all_departments, update_department, delete_department
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.crud.shift import create_shift, get_shift, get_all_shifts, update_shift, delete_shift
from app.schemas.project import *
from app.schemas.project_allocation import *
from app.schemas.shift import ShiftCreate, ShiftUpdate
from app.crud.designation import create_designation, get_designation, get_all_designations, update_designation, delete_designation
from app.schemas.designation import DesignationCreate, DesignationUpdate
from app.database import get_db
from app.crud.stats import get_counts
from app.schemas.stats import StatsResponse
from app.schemas.system_log import SystemLogResponse
from app.utils.attendance import determine_attendance_status
from app.utils.email import *


router = APIRouter(dependencies=[Depends(get_current_admin)])

# -------------STATS--------------


@router.get("/stats/", response_model=StatsResponse)
def get_statistics(db: Session = Depends(get_db)):
    return get_counts(db)

# --------------EMP---------------


@router.post("/employees/")
def create_new_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    print(employee.dict())
    return create_employee(db=db, employee=employee)


@router.get("/employees/{emp_id}")
def get_employee_by_code(emp_id: UUID, db: Session = Depends(get_db)):
    db_employee = get_employee(db=db, emp_id=emp_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.get("/employees/")
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_employees(db=db, skip=skip, limit=limit)


@router.put("/employees/{emp_id}")
def update_employee_details(emp_id: UUID, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = update_employee(db=db, emp_id=emp_id, employee=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.delete("/employees/{emp_id}")
def delete_employee_details(emp_id: UUID, db: Session = Depends(get_db)):
    db_employee = delete_employee(db=db, emp_id=emp_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.get("/employees/suggest-email-emp-code/{name}")
def suggest_email(name: str, db: Session = Depends(get_db)):
    return {"suggested_email": generate_unique_email(db, name), "suggested_emp_code": generate_emp_code(db, name)}

# ---------DEPT-------------------


@router.post("/departments/")
def create_new_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    return create_department(db=db, department=department)


@router.get("/departments/{dept_id}")
def get_department_by_id(dept_id: UUID, db: Session = Depends(get_db)):
    db_department = get_department(db=db, dept_id=dept_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department


@router.get("/departments/")
def list_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_departments(db=db, skip=skip, limit=limit)


@router.put("/departments/{dept_id}")
def update_department_details(dept_id: UUID, department: DepartmentUpdate, db: Session = Depends(get_db)):
    db_department = update_department(
        db=db, dept_id=dept_id, department=department)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department


@router.delete("/departments/{dept_id}")
def delete_department_details(dept_id: UUID, db: Session = Depends(get_db)):
    db_department = delete_department(db=db, dept_id=dept_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")


# -----------SHIFTS-----------
@router.post("/shifts/")
def create_new_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    return create_shift(db=db, shift=shift)


@router.get("/shifts/{shift_id}")
def get_shift_by_id(shift_id: UUID, db: Session = Depends(get_db)):
    db_shift = get_shift(db=db, shift_id=shift_id)
    if db_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return db_shift


@router.get("/shifts/")
def list_shifts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_shifts(db=db, skip=skip, limit=limit)


@router.put("/shifts/{shift_id}")
def update_shift_details(shift_id: UUID, shift: ShiftUpdate, db: Session = Depends(get_db)):
    db_shift = update_shift(db=db, shift_id=shift_id, shift=shift)
    if db_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return db_shift


@router.delete("/shifts/{shift_id}")
def delete_shift_details(shift_id: UUID, db: Session = Depends(get_db)):
    db_shift = delete_shift(db=db, shift_id=shift_id)
    if db_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return db_shift


# ------------DESIGNATIONS-------------
@router.post("/designations/")
def create_new_designation(designation: DesignationCreate, db: Session = Depends(get_db)):
    return create_designation(db=db, designation=designation)


@router.get("/designations/{designation_id}")
def get_designation_by_id(designation_id: UUID, db: Session = Depends(get_db)):
    db_designation = get_designation(db=db, designation_id=designation_id)
    if db_designation is None:
        raise HTTPException(status_code=404, detail="Designation not found")
    return db_designation


@router.get("/designations/")
def list_designations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_designations(db=db, skip=skip, limit=limit)


@router.put("/designations/{designation_id}")
def update_designation_details(designation_id: UUID, designation: DesignationUpdate, db: Session = Depends(get_db)):
    db_designation = update_designation(
        db=db, designation_id=designation_id, designation=designation)
    if db_designation is None:
        raise HTTPException(status_code=404, detail="Designation not found")
    return db_designation


@router.delete("/designations/{designation_id}")
def delete_designation_details(designation_id: UUID, db: Session = Depends(get_db)):
    db_designation = delete_designation(db=db, designation_id=designation_id)
    if db_designation is None:
        raise HTTPException(status_code=404, detail="Designation not found")
    return db_designation


# --------ANALYTICS----------
@router.get("/analytics/{emp_id}")
def get_employee_analytics(emp_id: str, start_date: str, end_date: str, db: Session = Depends(get_db)):
    time_wastage_data = calculate_time_wastage(
        db=db, emp_id=emp_id, end_date=end_date, start_date=start_date)
    return {"time_wastage_data": time_wastage_data}


# ---------CALENDAR---------------
@router.get("/attendance/calendar")
def get_attendance_calendar(
    emp_id: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    return get_attendance_calendar_data(
        db=db, emp_id=emp_id, start_date=start_date, end_date=end_date)


# ---------------SYSTEM LOGS----------------
@router.get("/system-logs/employee/{emp_id}", response_model=list[SystemLogResponse])
def get_logs_of_employee(emp_id: UUID, db: Session = Depends(get_db)):
    logs = get_logs_by_emp_id(db, emp_id)
    if not logs:
        raise HTTPException(
            status_code=404, detail="No logs found for this employee.")
    return logs


# Get system logs for an employee within a date range
@router.get("/system-logs/employee/{emp_id}/date-range", response_model=list[SystemLogResponse])
def get_system_logs_in_date_range(emp_id: UUID, start_date: date, end_date: date, db: Session = Depends(get_db)):
    logs = get_logs_by_emp_id_in_date_range(db, emp_id, start_date, end_date)
    if not logs:
        raise HTTPException(
            status_code=404, detail="No system logs found in the given date range.")
    return logs


# ----------BIOMETRIC LOGS-------------
# Get all biometric logs (optionally filter by emp_id)
@router.get("/biometric-logs", response_model=list[BiometricLogResponse])
def list_logs(emp_id: UUID = None, db: Session = Depends(get_db)):
    return get_biometric_logs(db, emp_id)


# Get a single biometric log by ID
@router.get("/biometric-logs/{log_id}", response_model=BiometricLogResponse)
def read_log(log_id: UUID, db: Session = Depends(get_db)):
    log = get_biometric_log(db, log_id)
    if log is None:
        raise HTTPException(status_code=404, detail="Biometric log not found")
    return log


# Get logs for a specific employee
@router.get("/biometric-logs/employee/{emp_id}", response_model=list[BiometricLogResponse])
def get_logs_by_employee(emp_id: UUID, db: Session = Depends(get_db)):
    logs = get_biometric_logs_by_employee(db, emp_id)
    if not logs:
        raise HTTPException(
            status_code=404, detail="No logs found for this employee")
    return logs


# Get biometric logs for an employee within a date range
@router.get("/biometric-logs/employee/{emp_id}/date-range", response_model=list[BiometricLogResponse])
def get_biometric_logs_in_date_range(emp_id: UUID, start_date: date, end_date: date, db: Session = Depends(get_db)):
    logs = get_employee_biometric_logs_by_date_range(
        db, emp_id, start_date, end_date)
    if not logs:
        raise HTTPException(
            status_code=404, detail="No biometric logs found in the given date range.")
    return logs


# Delete a biometric log by ID
@router.delete("/biometric-logs/{log_id}", response_model=BiometricLogResponse)
def delete_log(log_id: UUID, db: Session = Depends(get_db)):
    deleted_log = delete_biometric_log(db, log_id)
    if deleted_log is None:
        raise HTTPException(status_code=404, detail="Biometric log not found")
    return deleted_log


# Update a biometric log by ID
@router.put("/biometric-logs/{log_id}", response_model=BiometricLogResponse)
def update_log(log_id: UUID, biometric_log: BiometricLogUpdate, db: Session = Depends(get_db)):
    updated_log = update_biometric_log(db, log_id, biometric_log)
    if updated_log is None:
        raise HTTPException(status_code=404, detail="Biometric log not found")
    return updated_log


# ----------------PROJECTS-----------------
# Create a new project
@router.post("/projects/", response_model=ProjectResponse)
def create_project_api(project: ProjectCreate, db: Session = Depends(get_db)):
    return create_project(db, project)


# Get all projects
@router.get("/projects/", response_model=List[ProjectResponse])
def get_projects_api(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_projects(db, skip, limit)


# Get project by ID
@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project_api(project_id: str, db: Session = Depends(get_db)):
    db_project = get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


# Update a project
@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project_api(project_id: str, project: ProjectUpdate, db: Session = Depends(get_db)):
    db_project = update_project(db, project_id, project)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


# Delete a project
@router.delete("/projects/{project_id}", response_model=ProjectResponse)
def delete_project_api(project_id: str, db: Session = Depends(get_db)):
    db_project = delete_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


# Project Metadata
@router.get("/projects-metadata", response_model=ProjectMetadataResponse)
def get_project_metadata_api():
    return {
        "statuses": [status.name.upper() for status in list(ProjectStatus)],
        "priorities": [priority.name.upper() for priority in list(ProjectPriority)],
        "roles": [role.name.upper() for role in list(ProjectRole)],
        "allocation_statuses": [status.name.upper() for status in list(AllocationStatus)]
    }


# ----------PROJECT ALLOCATIONS------------
@router.post("/project-allocations/", response_model=ProjectAllocationResponse)
def assign_employee(allocation_data: ProjectAllocationCreate, db: Session = Depends(get_db)):
    """Assign an employee to a project"""
    return create_project_allocation(db, allocation_data)


@router.get("/project-allocations/{project_id}", response_model=list[ProjectAllocationResponse])
def get_allocations(project_id: UUID, db: Session = Depends(get_db)):
    """Get all allocations for a project"""
    return get_project_allocations(db, project_id)


@router.put("/project-allocations/{allocation_id}/status", response_model=ProjectAllocationResponse)
def update_allocation_status(allocation_id: UUID, status: AllocationStatus, db: Session = Depends(get_db)):
    """Update an employee's allocation status"""
    allocation = update_project_allocation_status(db, allocation_id, status)
    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")
    return allocation


@router.delete("/project-allocations/{allocation_id}")
def remove_allocation(allocation_id: UUID, db: Session = Depends(get_db)):
    """Remove an employee from a project"""
    allocation = remove_employee_from_project(db, allocation_id)
    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")
    return {"message": "Employee removed from project"}
