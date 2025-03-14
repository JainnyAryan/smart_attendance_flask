from sqlalchemy import Column, String, Text, Date, Integer, ARRAY, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
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
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())