from sqlalchemy import Column, Integer, String, Boolean
from app.database import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False) 
    is_admin = Column(Boolean, default=False) 