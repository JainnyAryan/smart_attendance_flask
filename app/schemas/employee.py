from uuid import UUID
from pydantic import BaseModel, EmailStr
from app.schemas.shift import ShiftResponse
from app.schemas.department import DepartmentResponse
from app.schemas.designation import DesignationResponse


class EmployeeBase(BaseModel):
    name: str
    emp_code: str
    email: EmailStr
    shift_id: UUID
    dept_id: UUID
    designation_id: UUID

class EmployeeCreate(EmployeeBase):
    pass
        

class EmployeeUpdate(BaseModel):
    name: str | None = None
    emp_code: str | None = None
    email: EmailStr | None = None
    shift_id: UUID | None = None
    dept_id: UUID | None = None
    designation_id: UUID | None = None

    class Config:
        from_attributes = True
        

class EmployeeResponse(EmployeeBase):
    id: UUID
    shift: ShiftResponse | None = None
    department: DepartmentResponse | None = None
    designation: DesignationResponse | None = None

    class Config:
        from_attributes = True
