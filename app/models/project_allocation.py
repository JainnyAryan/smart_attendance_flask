from sqlalchemy import UUID, Column, Date, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import BaseModel
import enum


class ProjectRole(enum.Enum):
    MANAGER = "MANAGER"  # Oversees the project
    TECH_LEAD = "TECH_LEAD"  # Leads technical decisions
    DEVELOPER = "DEVELOPER"  # Writes and maintains code
    DESIGNER = "DESIGNER"  # Works on UI/UX
    TESTER = "TESTER"  # Ensures quality through testing
    DATA_SCIENTIST = "DATA_SCIENTIST"  # Works on AI/ML parts
    BUSINESS_ANALYST = "BUSINESS_ANALYST"  # Defines project requirements
    INTERN = "INTERN"  # Assists in development/testing
    SUPPORT_ENGINEER = "SUPPORT_ENGINEER"  # Provides technical support


class AllocationStatus(enum.Enum):
    PENDING = "PENDING"  # Assigned but not yet started
    ACTIVE = "ACTIVE"  # Currently working on the project
    ON_HOLD = "ON_HOLD"  # Temporarily stopped working
    COMPLETED = "COMPLETED"  # Finished work on the project
    REMOVED = "REMOVED"  # Removed from the project


class ProjectAllocation(BaseModel):
    __tablename__ = "project_allocations"

    project_id = Column(UUID, ForeignKey(
        "projects.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(UUID, ForeignKey(
        "employees.id", ondelete="CASCADE"), nullable=False)

    # Employee role in project
    role = Column(Enum(ProjectRole), nullable=False)
    status = Column(Enum(AllocationStatus),
                    default=AllocationStatus.PENDING)  # Allocation status

    # When allocation was made
    allocated_on = Column(Date, default=datetime.utcnow)
    start_date = Column(Date, nullable=True)  # When employee actually starts
    deadline = Column(Date, nullable=False)  # Expected completion date
    # When the employee finished work
    completion_date = Column(Date, nullable=True)

    # Relationships
    project = relationship(
        "Project", back_populates="project_allocations", passive_deletes=True)
    employee = relationship(
        "Employee", back_populates="project_allocations", passive_deletes=True)
    status_logs = relationship(
        "ProjectAllocationStatusLog",
        back_populates="allocation",
        cascade="all, delete-orphan"
    )
