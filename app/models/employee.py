from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.database import BaseModel


class Employee(BaseModel):
    __tablename__ = 'employees'

    name = Column(String, index=True)
    emp_code = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    shift_id = Column(UUID(as_uuid=True), ForeignKey('shifts.id'))
    dept_id = Column(UUID(as_uuid=True), ForeignKey('departments.id'))
    designation_id = Column(UUID(as_uuid=True), ForeignKey('designations.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    system_logs = relationship("SystemLog", back_populates="employee")
    biometric_logs = relationship("BiometricLog", back_populates="employee")
    shift = relationship("Shift", back_populates="employees")
    department = relationship("Department", back_populates="employees")
    designation = relationship("Designation", back_populates="employees")
    user = relationship("User", back_populates="employee")
