from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).order_by(User.created_at.desc()).all()

def update_user(db: Session, email: str, user_update: UserUpdate):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return None
    
    if user_update.password:
        db_user.hashed_password = hash_password(user_update.password)
    if user_update.is_admin is not None:
        db_user.is_admin = user_update.is_admin
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, email: str):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user