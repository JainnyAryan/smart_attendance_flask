from pydantic import BaseModel
from uuid import UUID

class DepartmentBase(BaseModel):
    name: str
    dept_code: str

class DepartmentCreate(DepartmentBase):  # ✅ Used in POST requests
    pass

class DepartmentUpdate(BaseModel):  # ✅ Used in PUT requests
    name: str | None = None
    dept_code: str | None = None

class DepartmentResponse(DepartmentBase):  # ✅ Used in API responses
    id: UUID

    class Config:
        from_attributes = True