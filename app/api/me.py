from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.auth.auth import get_current_user
from app.database import get_db
from app.models.employee import Employee
from app.models.user import User

router = APIRouter()


@router.get("/me")
def get_current_user_info(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if (user.is_admin):
        return {"email": user.email, "is_admin": user.is_admin, "employee": None}
    else:
        employee = db.query(Employee).options(
            joinedload(Employee.shift),
            joinedload(Employee.department),
            joinedload(Employee.designation)
        ).filter(Employee.user_id == user.id).first()

        return {"email": user.email, "is_admin": user.is_admin, "employee": employee}
