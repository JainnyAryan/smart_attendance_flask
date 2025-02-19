from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, UUID
from sqlalchemy.orm import relationship
from app.database import BaseModel

class SystemLog(BaseModel):
    __tablename__ = 'system_logs'
    
    emp_id = Column(UUID(as_uuid=True), ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    
    employee = relationship("Employee", back_populates="system_logs", passive_deletes=True)