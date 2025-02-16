from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import BaseModel


class Department(BaseModel):
    __tablename__ = 'departments'

    dept_code = Column(String, unique=True, index=True)
    name = Column(String)

    employees = relationship("Employee", back_populates="department")
