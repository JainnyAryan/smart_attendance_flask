from pydantic import BaseModel
from uuid import UUID

class DesignationBase(BaseModel):
    name: str
    designation_code: str

class DesignationCreate(DesignationBase):  # ✅ Used in POST requests
    pass

class DesignationUpdate(BaseModel):  # ✅ Used in PUT requests
    name: str | None = None
    designation_code: str | None = None

class DesignationResponse(DesignationBase):  # ✅ Used in API responses
    id: UUID

    class Config:
        from_attributes = True