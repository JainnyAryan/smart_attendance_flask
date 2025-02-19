from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    is_admin: bool = False

class UserCreate(UserBase):
    password: str
    
class UserUpdate(BaseModel):
    password: str | None = None
    is_admin: bool | None = None
    
class UserLogin(BaseModel):
    email: str
    password: str
    
class UserResponse(UserBase):
    id: UUID
    # emp_id: UUID | None = None
    
    class Config:
        from_attributes = True  
    

