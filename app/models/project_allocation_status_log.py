from sqlalchemy import Column, DateTime, Enum, ForeignKey, Interval
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import BaseModel
# make sure your enum is imported
from app.models.project_allocation import AllocationStatus


class ProjectAllocationStatusLog(BaseModel):
    __tablename__ = "project_allocation_status_logs"

    allocation_id = Column(UUID(as_uuid=True), ForeignKey(
        "project_allocations.id", ondelete="CASCADE"))
    from_status = Column(Enum(AllocationStatus), nullable=False)
    to_status = Column(Enum(AllocationStatus), nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow)
    duration_spent = Column(Interval, nullable=True)  # time in previous status

    allocation = relationship(
        "ProjectAllocation", back_populates="status_logs")
