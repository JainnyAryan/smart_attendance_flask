from sqlalchemy import UUID, Column, Date, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import BaseModel
import enum


class ProjectRole(enum.Enum):
    MANAGER = "manager"  # Oversees the project
    TECH_LEAD = "tech_lead"  # Leads technical decisions
    DEVELOPER = "developer"  # Writes and maintains code
    DESIGNER = "designer"  # Works on UI/UX
    TESTER = "tester"  # Ensures quality through testing
    DATA_SCIENTIST = "data_scientist"  # Works on AI/ML parts
    BUSINESS_ANALYST = "business_analyst"  # Defines project requirements
    INTERN = "intern"  # Assists in development/testing
    SUPPORT_ENGINEER = "support_engineer"  # Provides technical support


class AllocationStatus(enum.Enum):
    PENDING = "pending"  # Assigned but not yet started
    ACTIVE = "active"  # Currently working on the project
    COMPLETED = "completed"  # Finished work on the project
    ON_HOLD = "on_hold"  # Temporarily stopped working
    REMOVED = "removed"  # Removed from the project


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
        "Project", back_populates="allocations", cascade="all, delete")
    employee = relationship(
        "Employee", back_populates="allocations", cascade="all, delete")
