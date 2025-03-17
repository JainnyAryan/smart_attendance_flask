import enum
from sqlalchemy import Column, String, Text, Date, Integer, ARRAY, Enum
from app.database import BaseModel
from sqlalchemy.orm import mapped_column


class ProjectStatus(enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"


class ProjectPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Project(BaseModel):
    __tablename__ = "projects"

    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    status = Column(Enum(ProjectStatus), nullable=False,
                    default=ProjectStatus.PLANNED)
    priority = Column(Enum(ProjectPriority), nullable=False,
                      default=ProjectPriority.MEDIUM)
    max_team_size = Column(Integer)
    required_skills = Column(ARRAY(String))
    min_experience = Column(Integer, default=0)
