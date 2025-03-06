from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.system_log import *
from app.schemas.system_log import *
from ..database import get_db


router = APIRouter()


#----------SYSTEM lOG------------
@router.post("/system-log/in", response_model=SystemLogResponse)
def log_in(log: SystemLogIn, db: Session = Depends(get_db)):
    return create_log_in(db, log)



@router.post("/system-log/out", response_model=SystemLogResponse)
def log_out(log: SystemLogOut, db: Session = Depends(get_db)):
    try:
        return create_log_out(db, log)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Active session not found.")


@router.get("/system-log/employee/{emp_id}", response_model=list[SystemLogResponse])
def logs_by_employee(emp_id: UUID, db: Session = Depends(get_db)):
    logs = get_logs_by_emp_id(db, emp_id)
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for this employee.")
    return logs


@router.delete("/system-log/{log_id}", response_model=SystemLogResponse)
def remove_log(log_id: UUID, db: Session = Depends(get_db)):
    log = delete_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found.")
    return log