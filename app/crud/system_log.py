from sqlalchemy import Date, cast
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models.system_log import SystemLog
from app.schemas.system_log import SystemLogIn, SystemLogOut
from uuid import UUID
from datetime import date, datetime


def create_log_in(db: Session, log: SystemLogIn):
    db_log = SystemLog(
        emp_id=log.emp_id,
        in_ip_address=log.ip_address,
        start_time=log.start_time
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def create_log_out(db: Session, log: SystemLogOut):
    log_entry = db.query(SystemLog).filter(
        SystemLog.emp_id == log.emp_id,
        SystemLog.end_time.is_(None)
    ).first()

    if not log_entry:
        raise NoResultFound("No active session found for the employee.")

    log_entry.end_time = log.end_time
    log_entry.out_ip_address = log.ip_address
    db.commit()
    db.refresh(log_entry)
    return log_entry


def get_all_logs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(SystemLog).offset(skip).limit(limit).order_by(SystemLog.created_at.desc()).all()


def get_logs_by_emp_id(db: Session, emp_id: UUID):
    return db.query(SystemLog).filter(SystemLog.emp_id == emp_id).order_by(SystemLog.created_at.desc()).all()


def get_logs_by_emp_id_in_date_range(db: Session, emp_id: UUID, start_date: date, end_date: date):
    return db.query(SystemLog).filter(
        SystemLog.emp_id == emp_id,
        cast(SystemLog.start_time, Date) >= start_date,
        cast(SystemLog.end_time, Date) <= end_date
    ).order_by(SystemLog.created_at.desc()).all()


def delete_log(db: Session, log_id: UUID):
    log = db.query(SystemLog).filter(SystemLog.id == log_id).first()
    if log:
        db.delete(log)
        db.commit()
    return log
