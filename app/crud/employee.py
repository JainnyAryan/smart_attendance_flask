import random
import string
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeUpdate
from .user import *
from ..schemas.user import *



def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    password = "".join(random.choices(
        string.ascii_letters + string.digits, k=15))
    create_user(db, UserCreate(is_admin=False,
                email=db_employee.email, password=password))
    print(db_employee.email, password)
    return db_employee


def get_employee(db: Session, emp_id: UUID):
    return db.query(Employee).options(
        joinedload(Employee.shift),  
        joinedload(Employee.department), 
        joinedload(Employee.designation) 
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
        delete_user(db, db_employee.email)
    return db_employee
