from uuid import UUID
from pydantic import BaseModel
from app.schemas.shift import ShiftResponse
from app.schemas.department import DepartmentResponse
from app.schemas.designation import DesignationResponse


class EmployeeCreate(BaseModel):
    name: str
    shift_id: UUID
    dept_id: UUID
    designation_id: UUID

class EmployeeOut(EmployeeCreate):
    emp_id: UUID

    class Config:
        from_attributes = True

class EmployeeUpdate(BaseModel):
    name: str | None = None  
    shift_id: UUID | None = None  
    dept_id: UUID | None = None  
    designation_id: UUID | None = None 

    class Config:
        from_attributes = True
        
class EmployeeBase(BaseModel):
    name: str


class EmployeeResponse(EmployeeBase):  
    id: UUID
    shift: ShiftResponse | None = None
    department: DepartmentResponse | None = None
    designation: DesignationResponse | None = None

    class Config:
        from_attributes = True  