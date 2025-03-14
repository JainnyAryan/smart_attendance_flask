from uuid import UUID
from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

class ProjectBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    status: Optional[str] = "planned"
    priority: Optional[str] = "medium"
    max_team_size: Optional[int] = None
    required_skills: Optional[List[str]] = []
    min_experience: Optional[int] = 0

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True