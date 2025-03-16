from sqlalchemy.orm import Session
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate

def create_department(db: Session, department: DepartmentCreate):
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def get_department(db: Session, dept_id):
    return db.query(Department).filter(Department.id == dept_id).first()

def get_all_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Department).order_by(Department.created_at.desc()).offset(skip).limit(limit).all()

def update_department(db: Session, dept_id, department: DepartmentUpdate):
    db_department = get_department(db, dept_id)
    if db_department:
        for key, value in department.dict(exclude_unset=True).items():
            setattr(db_department, key, value)
        db.commit()
        db.refresh(db_department)
    return db_department

def delete_department(db: Session, dept_id):
    db_department = get_department(db, dept_id)
    if db_department:
        db.delete(db_department)
        db.commit()
    return db_department