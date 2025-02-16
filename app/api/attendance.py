from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..crud.employee import create_employee, get_employee
from ..schemas.employee import EmployeeCreate, EmployeeOut
from ..database import get_db

router = APIRouter()

@router.post("/employees/", response_model=EmployeeOut)
def create_employee_view(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db=db, employee=employee)

@router.get("/employees/{emp_id}", response_model=EmployeeOut)
def get_employee_view(emp_id: UUID, db: Session = Depends(get_db)):
    return get_employee(db=db, emp_id=emp_id)