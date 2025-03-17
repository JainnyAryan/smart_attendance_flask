import uuid
from sqlalchemy import TIMESTAMP, create_engine, Column, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), index=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
