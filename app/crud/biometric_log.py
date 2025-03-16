from datetime import date
from sqlalchemy import Date, cast
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models.biometric_log import BiometricLog
from app.schemas.biometric_log import BiometricLogCreate, BiometricLogUpdate
from uuid import UUID


# Create a new biometric log entry
def create_biometric_log(db: Session, biometric_log: BiometricLogCreate):
    db_log = BiometricLog(**biometric_log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


# Get a single biometric log by ID
def get_biometric_log(db: Session, log_id: UUID):
    return db.query(BiometricLog).filter(BiometricLog.id == log_id).first()


# Get all biometric logs (with optional emp_id filter)
def get_biometric_logs(db: Session, emp_id: UUID = None):
    query = select(BiometricLog)
    if emp_id:
        query = query.filter(BiometricLog.emp_id == emp_id)
    return db.execute(query.order_by(BiometricLog.in_time.desc())).scalars().all()

# Get biometric logs for a specific employee


def get_biometric_logs_by_employee(db: Session, emp_id: UUID):
    return db.query(BiometricLog).filter(BiometricLog.emp_id == emp_id).order_by(BiometricLog.in_time.desc()).all()


def get_employee_biometric_logs_by_date_range(db: Session, emp_id: UUID, start_date: date, end_date: date):
    return db.query(BiometricLog).filter(
        BiometricLog.emp_id == emp_id,
        cast(BiometricLog.in_time, Date) >= start_date,
        cast(BiometricLog.out_time, Date) <= end_date
    ).order_by(BiometricLog.in_time.desc()).all()


# Update biometric log (by ID)
def update_biometric_log(db: Session, log_id: UUID, biometric_log: BiometricLogUpdate):
    db_log = db.query(BiometricLog).filter(BiometricLog.id == log_id).first()
    if db_log:
        for key, value in biometric_log.model_dump(exclude_unset=True).items():
            setattr(db_log, key, value)
        db.commit()
        db.refresh(db_log)
    return db_log


# Delete biometric log by ID
def delete_biometric_log(db: Session, log_id: UUID):
    db_log = db.query(BiometricLog).filter(BiometricLog.id == log_id).first()
    if db_log:
        db.delete(db_log)
        db.commit()
    return db_log
