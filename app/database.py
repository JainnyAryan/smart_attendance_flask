import uuid
from sqlalchemy import create_engine, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL 

Base = declarative_base() 

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class BaseModel(Base):
    __abstract__ = True  
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()