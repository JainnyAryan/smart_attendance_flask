from sqlalchemy.orm import Session
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectUpdate

# Create a new project
def create_project(db: Session, project: ProjectCreate):
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# Get a project by ID
def get_project(db: Session, project_id: str):
    return db.query(Project).filter(Project.id == project_id).first()

# Get all projects
def get_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()

# Update a project
def update_project(db: Session, project_id: str, project: ProjectUpdate):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        for key, value in project.model_dump(exclude_unset=True).items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
    return db_project

# Delete a project
def delete_project(db: Session, project_id: str):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project