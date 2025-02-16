from sqlalchemy import Column, Integer, String, Boolean
from app.database import BaseModel
from sqlalchemy.orm import relationship

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False) 
    is_admin = Column(Boolean, default=False) 
    
    employee = relationship("Employee", back_populates="user")