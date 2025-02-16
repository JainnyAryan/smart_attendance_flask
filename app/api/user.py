from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.user import create_user, get_user_by_email, get_all_users, update_user, delete_user
from app.schemas.user import UserCreate, UserUpdate

router = APIRouter()

@router.post("/users/")
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@router.get("/users/{email}")
def get_user(email: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/")
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_users(db, skip, limit)

@router.put("/users/{email}")
def update_user_details(email: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db, email, user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{email}")
def delete_user_account(email: str, db: Session = Depends(get_db)):
    db_user = delete_user(db, email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}