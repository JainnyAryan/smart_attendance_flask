from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    status: str = "planned"
    priority: str = "medium"
    max_team_size: Optional[int] = None
    required_skills: Optional[List[str]] = []
    min_experience: Optional[int] = 0

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: str
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True