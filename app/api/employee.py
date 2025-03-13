from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.system_log import *
from app.schemas.system_log import *
from ..database import get_db

from app.schemas.biometric_log import BiometricLogCreate, BiometricLogResponse, BiometricLogUpdate
from app.crud.biometric_log import *


router = APIRouter()


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


@router.get("/system-log/employee/latest/{emp_id}", response_model=list[SystemLogResponse])
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




