from sqlalchemy import Column, String, Text, Date, Integer, ARRAY, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from ..database import BaseModel


class Project(BaseModel):
    __tablename__ = "projects"

    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    status = Column(String(20), nullable=False, default="planned")
    priority = Column(String(20), default="medium")
    max_team_size = Column(Integer)
    required_skills = Column(ARRAY(String))
    min_experience = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now())
