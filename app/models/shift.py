from sqlalchemy import Column, String, Time, DECIMAL, Integer
from sqlalchemy.orm import relationship
from app.database import BaseModel


class Shift(BaseModel):
    __tablename__ = "shifts"

    shift_code = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    break_time = Column(DECIMAL(5, 2), default=0.00)
    total_hours = Column(DECIMAL(5, 2), nullable=False)
    half_day_shift_hours = Column(
        DECIMAL(5, 2), nullable=False)  
    late_coming_mins = Column(DECIMAL(5, 2), nullable=False)
    early_going_mins = Column(DECIMAL(5, 2), nullable=False)
    same_day = Column(Integer, default=1) 

    employees = relationship("Employee", back_populates="shift", cascade="all, delete")
