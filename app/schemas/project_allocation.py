from uuid import UUID
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from app.models.project_allocation import ProjectRole, AllocationStatus

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

    class Config:
        from_attributes = True
