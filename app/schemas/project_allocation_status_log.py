from pydantic import BaseModel

from app.models.project_allocation import AllocationStatus


class AllocationStatusUpdateRequest(BaseModel):
    status: str
    
from datetime import datetime, timedelta
from pydantic import BaseModel
from enum import Enum

class AllocationStatusLogResponse(BaseModel):
    from_status: AllocationStatus
    to_status: AllocationStatus
    changed_at: datetime
    duration_spent: timedelta | None

    class Config:
        orm_mode = True