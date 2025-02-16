from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.models.department import Department
from app.models.shift import Shift
from app.models.designation import Designation

def get_counts(db: Session):
    return {
        "employee_count": db.query(Employee).count(),
        "department_count": db.query(Department).count(),
        "shift_count": db.query(Shift).count(),
        "designation_count": db.query(Designation).count(),
    }