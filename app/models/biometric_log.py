from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, UUID
from sqlalchemy.orm import relationship
from app.database import BaseModel


class BiometricLog(BaseModel):
    __tablename__ = 'biometric_logs'

    emp_id = Column(UUID(as_uuid=True), ForeignKey(
        'employees.id', ondelete='CASCADE'), nullable=False)
    in_time = Column(TIMESTAMP)
    out_time = Column(TIMESTAMP)

    employee = relationship(
        "Employee", back_populates="biometric_logs", passive_deletes=True)
