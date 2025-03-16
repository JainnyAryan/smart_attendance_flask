from sqlalchemy.orm import Session
from app.models.designation import Designation
from app.schemas.designation import DesignationCreate, DesignationUpdate

def create_designation(db: Session, designation: DesignationCreate):
    db_designation = Designation(**designation.dict())
    db.add(db_designation)
    db.commit()
    db.refresh(db_designation)
    return db_designation

def get_designation(db: Session, designation_id):
    return db.query(Designation).filter(Designation.id == designation_id).first()

def get_all_designations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Designation).offset(skip).limit(limit).order_by(Designation.created_at.desc()).all()

def update_designation(db: Session, designation_id, designation: DesignationUpdate):
    db_designation = get_designation(db, designation_id)
    if db_designation:
        for key, value in designation.dict(exclude_unset=True).items():
            setattr(db_designation, key, value)
        db.commit()
        db.refresh(db_designation)
    return db_designation

def delete_designation(db: Session, designation_id):
    db_designation = get_designation(db, designation_id)
    if db_designation:
        db.delete(db_designation)
        db.commit()
    return db_designation