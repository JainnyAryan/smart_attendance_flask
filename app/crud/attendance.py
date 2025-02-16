from sqlalchemy.orm import Session
from datetime import datetime
from ..models.system_log import SystemLog
from ..models.biometric_log import BiometricLog
from ..schemas.attendance import AttendanceIn, AttendanceOut

def log_attendance_in(db: Session, attendance_in: AttendanceIn):
    db_log = SystemLog(emp_id=attendance_in.emp_id, start_time=attendance_in.start_time, end_time=None)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def log_attendance_out(db: Session, attendance_out: AttendanceOut):
    db_log = db.query(SystemLog).filter(SystemLog.emp_id == attendance_out.emp_id, SystemLog.end_time == None).first()
    db_log.end_time = attendance_out.end_time
    db.commit()
    db.refresh(db_log)
    return db_log