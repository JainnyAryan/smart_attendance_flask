from sqlalchemy import func
from sqlalchemy.orm import Session
from app.crud.attendance import get_attendance_calendar_data
from app.models.employee import Employee
from datetime import datetime, timedelta

from app.models.project import Project

def get_attendance_stats(db: Session, name: str):
    res = db.query(Employee).filter(func.lower(Employee.name).ilike(name))
    emp = res.first()
    
    if not emp:
        return None

    end_date = datetime.today().date().strftime("%Y-%m-%d")  # Convert to string
    start_date = (datetime.today().date() - timedelta(days=30)).strftime("%Y-%m-%d")  # Convert to string

    return get_attendance_calendar_data(db=db, emp_id=emp.id, start_date=start_date, end_date=end_date)


def get_all_projects(db: Session):
    res = db.query(Project).order_by(Project.created_at.desc()).all()
    return res