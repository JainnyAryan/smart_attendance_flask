from sqlalchemy.orm import Session
from app.models.shift import Shift
from app.schemas.shift import ShiftCreate, ShiftUpdate

def create_shift(db: Session, shift: ShiftCreate):
    db_shift = Shift(**shift.dict())
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift

def get_shift(db: Session, shift_id):
    return db.query(Shift).filter(Shift.id == shift_id).first()

def get_all_shifts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Shift).order_by(Shift.created_at.desc()).offset(skip).limit(limit).all()

def update_shift(db: Session, shift_id, shift: ShiftUpdate):
    db_shift = get_shift(db, shift_id)
    if db_shift:
        for key, value in shift.dict(exclude_unset=True).items():
            setattr(db_shift, key, value)
        db.commit()
        db.refresh(db_shift)
    return db_shift

def delete_shift(db: Session, shift_id):
    db_shift = get_shift(db, shift_id)
    if db_shift:
        db.delete(db_shift)
        db.commit()
    return db_shift