from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud.employee import create_employee, get_employee
from ..schemas.employee import EmployeeCreate, EmployeeResponse

router = APIRouter()


@router.get("/employees/{emp_id}", response_model=EmployeeResponse)
def get_employee_view(emp_id: UUID, db: Session = Depends(get_db)):
    employee = get_employee(db=db, emp_id=emp_id)
    return EmployeeResponse(id=employee.id, name=employee.name, emp_code=employee.emp_code,
                            email=employee.email, shift_id=employee.shift_id,
                            dept_id=employee.dept_id, designation_id=employee.designation_id,
                            designation=employee.designation, department=employee.department,
                            shift=employee.shift
                            )



