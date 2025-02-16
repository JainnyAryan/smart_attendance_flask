from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False
    
class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    is_admin: bool

    class Config:
        from_attributes = True  