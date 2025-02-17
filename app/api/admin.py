from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.employee import create_employee, get_employee, get_all_employees, update_employee, delete_employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.crud.department import create_department, get_department, get_all_departments, update_department, delete_department
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.crud.shift import create_shift, get_shift, get_all_shifts, update_shift, delete_shift
from app.schemas.shift import ShiftCreate, ShiftUpdate
from app.crud.designation import create_designation, get_designation, get_all_designations, update_designation, delete_designation
from app.schemas.designation import DesignationCreate, DesignationUpdate
from app.database import get_db
from app.crud.stats import get_counts
from app.schemas.stats import StatsResponse
from app.utils.email import *

router = APIRouter()

# -------------STATS--------------


@router.get("/stats/", response_model=StatsResponse)
def get_statistics(db: Session = Depends(get_db)):
    return get_counts(db)

# --------------EMP---------------


@router.post("/employees/")
def create_new_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    print(employee.dict())
    return create_employee(db=db, employee=employee)


@router.get("/employees/{emp_id}")
def get_employee_by_code(emp_id: UUID, db: Session = Depends(get_db)):
    db_employee = get_employee(db=db, emp_id=emp_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.get("/employees/")
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_employees(db=db, skip=skip, limit=limit)


@router.put("/employees/{emp_id}")
def update_employee_details(emp_id: UUID, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = update_employee(db=db, emp_id=emp_id, employee=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.delete("/employees/{emp_id}")
def delete_employee_details(emp_id: UUID, db: Session = Depends(get_db)):
    db_employee = delete_employee(db=db, emp_id=emp_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.get("/employees/suggest-email-emp-code/{name}")
def suggest_email(name: str, db: Session = Depends(get_db)):
    return {"suggested_email": generate_unique_email(db, name), "suggested_emp_code" : generate_emp_code(db, name)}

# ---------DEPT-------------------


@router.post("/departments/")
def create_new_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    return create_department(db=db, department=department)


@router.get("/departments/{dept_id}")
def get_department_by_id(dept_id: UUID, db: Session = Depends(get_db)):
    db_department = get_department(db=db, dept_id=dept_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department


@router.get("/departments/")
def list_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_departments(db=db, skip=skip, limit=limit)


@router.put("/departments/{dept_id}")
def update_department_details(dept_id: UUID, department: DepartmentUpdate, db: Session = Depends(get_db)):
    db_department = update_department(
        db=db, dept_id=dept_id, department=department)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department


@router.delete("/departments/{dept_id}")
def delete_department_details(dept_id: UUID, db: Session = Depends(get_db)):
    db_department = delete_department(db=db, dept_id=dept_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")


# -----------SHIFTS-----------
@router.post("/shifts/")
def create_new_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    return create_shift(db=db, shift=shift)


@router.get("/shifts/{shift_id}")
def get_shift_by_id(shift_id: UUID, db: Session = Depends(get_db)):
    db_shift = get_shift(db=db, shift_id=shift_id)
    if db_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return db_shift


@router.get("/shifts/")
def list_shifts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_shifts(db=db, skip=skip, limit=limit)


@router.put("/shifts/{shift_id}")
def update_shift_details(shift_id: UUID, shift: ShiftUpdate, db: Session = Depends(get_db)):
    db_shift = update_shift(db=db, shift_id=shift_id, shift=shift)
    if db_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return db_shift


@router.delete("/shifts/{shift_id}")
def delete_shift_details(shift_id: UUID, db: Session = Depends(get_db)):
    db_shift = delete_shift(db=db, shift_id=shift_id)
    if db_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return db_shift


# ------------DESIGNATIONS-------------
@router.post("/designations/")
def create_new_designation(designation: DesignationCreate, db: Session = Depends(get_db)):
    return create_designation(db=db, designation=designation)


@router.get("/designations/{designation_id}")
def get_designation_by_id(designation_id: UUID, db: Session = Depends(get_db)):
    db_designation = get_designation(db=db, designation_id=designation_id)
    if db_designation is None:
        raise HTTPException(status_code=404, detail="Designation not found")
    return db_designation


@router.get("/designations/")
def list_designations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_designations(db=db, skip=skip, limit=limit)


@router.put("/designations/{designation_id}")
def update_designation_details(designation_id: UUID, designation: DesignationUpdate, db: Session = Depends(get_db)):
    db_designation = update_designation(
        db=db, designation_id=designation_id, designation=designation)
    if db_designation is None:
        raise HTTPException(status_code=404, detail="Designation not found")
    return db_designation


@router.delete("/designations/{designation_id}")
def delete_designation_details(designation_id: UUID, db: Session = Depends(get_db)):
    db_designation = delete_designation(db=db, designation_id=designation_id)
    if db_designation is None:
        raise HTTPException(status_code=404, detail="Designation not found")
    return db_designation
