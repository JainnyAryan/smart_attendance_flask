from datetime import timedelta
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.auth.auth import get_current_admin
from app.crud.analytics import calculate_time_wastage
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
from app.utils.attendance import determine_attendance_status
from app.utils.email import *


router = APIRouter(dependencies=[Depends(get_current_admin)])

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
    return {"suggested_email": generate_unique_email(db, name), "suggested_emp_code": generate_emp_code(db, name)}

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


# --------ANALYTICS----------
@router.get("/analytics/{emp_id}")
def get_employee_analytics(emp_id: str, start_date: str, end_date: str, db: Session = Depends(get_db)):
    time_wastage_data = calculate_time_wastage(
        db=db, emp_id=emp_id, end_date=end_date, start_date=start_date)
    return {"time_wastage_data": time_wastage_data}


# ---------CALENDAR---------------
@router.get("/attendance/calendar")
def get_attendance_calendar(
    emp_id: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    try:
        # Convert string dates to datetime.date
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # SQL Query to fetch biometric logs and shifts
        query = text("""
            SELECT 
                b.in_time,
                b.out_time,
                b.in_time::date AS log_date,
                s.start_time,
                s.end_time,
                s.total_hours,
                s.half_day_shift_hours
            FROM biometric_logs b
            LEFT JOIN employees e ON b.emp_id = e.id
            LEFT JOIN shifts s ON e.shift_id = s.id
            WHERE b.emp_id = :emp_id
              AND b.in_time::date BETWEEN :start_date AND :end_date
            ORDER BY log_date;
        """)

        # Execute query and get results with key-based access
        results = db.execute(query, {
            "emp_id": emp_id,
            "start_date": start_date,
            "end_date": end_date
        }).mappings().all()  # <-- Converts rows to key-value dicts

        # Prepare attendance data
        calendar_data = {}

        # Calculate attendance status for each result
        for result in results:
            log_date = result["log_date"]
            status = determine_attendance_status(
                result["in_time"],
                result["out_time"],
                result["start_time"],
                result["end_time"],
                result["total_hours"],
                result["half_day_shift_hours"]
            )
            calendar_data[log_date] = status

        # Ensure all dates are covered
        current_date = parsed_start_date
        while current_date <= parsed_end_date:
            if current_date not in calendar_data:
                calendar_data[current_date] = "Absent"
            current_date += timedelta(days=1)

        # Format for frontend
        formatted_calendar = [
            {"date": str(date), "status": status}
            for date, status in sorted(calendar_data.items())
        ]

        return {"employee_id": emp_id, "calendar": formatted_calendar}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Attendance logic
