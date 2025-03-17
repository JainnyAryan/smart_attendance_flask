from uuid import UUID
from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Optional
from app.models.project_allocation import ProjectRole, AllocationStatus
from app.schemas.employee import EmployeeResponse
from app.schemas.project import ProjectResponse

# Request Schema (Used when adding/updating allocation)
class ProjectAllocationCreate(BaseModel):
    project_id: UUID
    employee_id: UUID
    role: ProjectRole
    status: Optional[AllocationStatus] = AllocationStatus.PENDING
    allocated_on: Optional[date] = None
    deadline: Optional[date] = None


# Response Schema
class ProjectAllocationResponse(ProjectAllocationCreate):
    id: UUID
    project: ProjectResponse
    employee: EmployeeResponse
    
    @field_validator("role", "status", mode="before")
    @classmethod
    def to_uppercase(cls, value: Optional[str]) -> Optional[str]:
        return value.name.upper() if value else None

    class Config:
        from_attributes = True
