import enum
from sqlalchemy import Column, String, Text, Date, Integer, ARRAY, Enum
from app.database import BaseModel
from sqlalchemy.orm import mapped_column, relationship


class ProjectStatus(enum.Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"


class ProjectPriority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


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

    project_allocations = relationship(
        "ProjectAllocation", back_populates="project", cascade="all, delete")
