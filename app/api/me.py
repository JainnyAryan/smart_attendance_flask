from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.auth import get_current_user
from app.database import get_db

router = APIRouter()

@router.get("/me")
def get_current_user_info(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return {"email": user.email, "is_admin": user.is_admin}