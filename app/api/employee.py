from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..crud.attendance import log_attendance_in, log_attendance_out
from ..schemas.attendance import AttendanceIn, AttendanceOut
from ..database import get_db

router = APIRouter()

@router.post("/attendance/login")
def log_in(attendance_in: AttendanceIn, db: Session = Depends(get_db)):
    return log_attendance_in(db=db, attendance_in=attendance_in)

@router.post("/attendance/logout")
def log_out(attendance_out: AttendanceOut, db: Session = Depends(get_db)):
    return log_attendance_out(db=db, attendance_out=attendance_out)