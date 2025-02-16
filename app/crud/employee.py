from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeUpdate

def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employee(db: Session, emp_id: UUID):
    return db.query(Employee).options(
        joinedload(Employee.shift),  # Load shift data
        joinedload(Employee.department),  # Load department data
        joinedload(Employee.designation)  # Load designation data
    ).filter(Employee.id == emp_id).first()

def get_all_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Employee).options(
        joinedload(Employee.shift),
        joinedload(Employee.department),
        joinedload(Employee.designation)
    ).offset(skip).limit(limit).all()
def update_employee(db: Session, emp_id: UUID, employee: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.id == emp_id).first()
    if db_employee:
        for key, value in employee.dict(exclude_unset=True).items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, emp_id: UUID):
    db_employee = db.query(Employee).filter(Employee.id == emp_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee