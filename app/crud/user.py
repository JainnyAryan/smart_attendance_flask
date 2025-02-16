from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to create a new user (register)
def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)  # Hash the password before storing
    db_user = User(username=user.username, hashed_password=hashed_password, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Function to get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()