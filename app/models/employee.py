from sqlalchemy import ARRAY, Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.database import BaseModel
from app.models.system_log import SystemLog
from app.models.biometric_log import BiometricLog
from app.models.shift import Shift
from app.models.department import Department
from app.models.designation import Designation
from app.models.user import User
from app.models.project_allocation import ProjectAllocation
from app.models.project_allocation_status_log import ProjectAllocationStatusLog


class Employee(BaseModel):
    __tablename__ = 'employees'

    name = Column(String, index=True)
    emp_code = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    skills = Column(ARRAY(String))
    experience = Column(Integer, default=0)
    shift_id = Column(UUID(as_uuid=True), ForeignKey(
        'shifts.id', ondelete='CASCADE'), nullable=False)
    dept_id = Column(UUID(as_uuid=True), ForeignKey(
        'departments.id', ondelete='CASCADE'), nullable=False)
    designation_id = Column(UUID(as_uuid=True), ForeignKey(
        'designations.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    system_logs = relationship(
        "SystemLog", back_populates="employee", cascade="all, delete")
    biometric_logs = relationship(
        "BiometricLog", back_populates="employee", cascade="all, delete")
    shift = relationship(
        "Shift", back_populates="employees", passive_deletes=True)
    department = relationship(
        "Department", back_populates="employees", passive_deletes=True)
    designation = relationship(
        "Designation", back_populates="employees", passive_deletes=True)
    user = relationship("User", back_populates="employee",
                        passive_deletes=True)
    project_allocations = relationship(
        "ProjectAllocation", back_populates="employee", cascade="all, delete")
