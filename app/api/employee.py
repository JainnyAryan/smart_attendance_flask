from app.crud.project_allocation_status_log import log_update_allocation_status
from app.models.employee import Employee
from app.schemas.project_allocation import ProjectAllocationResponse
from app.crud.project_allocation import get_allocation_statuses, get_allocations_by_employee_id, update_project_allocation_status
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user
from app.crud.system_log import *
from app.models.user import User
from app.schemas.project_allocation_status_log import AllocationStatusUpdateRequest
from app.schemas.system_log import *
from ..database import get_db

from app.schemas.biometric_log import BiometricLogCreate, BiometricLogResponse, BiometricLogUpdate
from app.crud.biometric_log import *


router = APIRouter(dependencies=[Depends(get_current_user)])


# ----------SYSTEM lOG------------
@router.post("/system-log/in", response_model=SystemLogResponse)
def log_in(log: SystemLogIn, db: Session = Depends(get_db)):
    return create_log_in(db, log)


@router.post("/system-log/out", response_model=SystemLogResponse)
def log_out(log: SystemLogOut, db: Session = Depends(get_db)):
    try:
        return create_log_out(db, log)
    except NoResultFound:
        raise HTTPException(
            status_code=404, detail="Active session not found.")


@router.get("/system-log/employee/latest/{emp_id}", response_model=SystemLogResponse)
def latest_log_of_employee(emp_id: UUID, db: Session = Depends(get_db)):
    logs = get_logs_by_emp_id(db, emp_id)
    if not logs:
        raise HTTPException(
            status_code=404, detail="No logs found for this employee.")
    return logs[0]


@router.delete("/system-log/{log_id}", response_model=SystemLogResponse)
def remove_log(log_id: UUID, db: Session = Depends(get_db)):
    log = delete_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found.")
    return log

# -------------BIOMETRIC LOGS-------------------


# Create a new biometric log
@router.post("/biometric-logs", response_model=BiometricLogResponse)
def create_log(biometric_log: BiometricLogCreate, db: Session = Depends(get_db)):
    return create_biometric_log(db, biometric_log)


# Get logs for a specific employee
@router.get("/biometric-logs/employee/latest/{emp_id}", response_model=list[BiometricLogResponse])
def get_latest_log_by_employee(emp_id: UUID, db: Session = Depends(get_db)):
    logs = get_biometric_logs_by_employee(db, emp_id)
    if not logs:
        raise HTTPException(
            status_code=404, detail="No logs found for this employee")
    return logs[0]


# ----------------PROJECT ALLOCATIONS----------------

@router.get("/my-project-allocations/", response_model=list[ProjectAllocationResponse])
def get_allocations_for_employee(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    employees : list[Employee] = user.employee
    emp_id = employees[0].id if employees else None
    if not emp_id:
        raise HTTPException(status_code=400, detail="User is not associated with any employee.")
    allocations = get_allocations_by_employee_id(db, emp_id)
    if not allocations:
        raise HTTPException(
            status_code=404, detail="No allocations found for this employee.")
    return allocations

@router.get("/allocation-statuses", response_model=list[str])
def get_project_allocation_statuses(db: Session = Depends(get_db)):
    return get_allocation_statuses()

@router.put("/allocations/{allocation_id}/status", response_model=ProjectAllocationResponse)
def update_allocation_status_endpoint(
    allocation_id: UUID,
    payload: AllocationStatusUpdateRequest,
    db: Session = Depends(get_db)
):
    log_update_allocation_status(db, allocation_id, payload.status)
    updated_allocation = update_project_allocation_status(db, allocation_id, payload.status)
    return updated_allocation
