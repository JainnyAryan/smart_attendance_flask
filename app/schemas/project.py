from uuid import UUID
from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import List, Optional
from app.models.project import ProjectStatus, ProjectPriority



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


class ProjectUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    max_team_size: Optional[int] = None
    required_skills: Optional[List[str]] = None
    min_experience: Optional[int] = None


class ProjectResponse(ProjectBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    @field_validator("status", "priority", mode="before")
    @classmethod
    def to_uppercase(cls, value: Optional[str]) -> Optional[str]:
        return value.name.upper() if value else None

    class Config:
        from_attributes = True


class ProjectMetadataResponse(BaseModel):
    statuses : List[str]
    priorities : List[str]
    roles : List[str]
    allocation_statuses : List[str]
    
    class Config:
        from_attributes = True