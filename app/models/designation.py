from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import BaseModel

class Designation(BaseModel):
    __tablename__ = "designations"

    designation_code = Column(String, index=True)
    name = Column(String, unique=True, nullable=False)

    employees = relationship("Employee", back_populates="designation")  