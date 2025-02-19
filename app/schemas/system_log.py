from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from app.schemas.employee import EmployeeResponse


class SystemLogResponse(BaseModel):
    id: UUID
    employee: EmployeeResponse
    start_time: datetime | None
    end_time: datetime | None

    class Config:
        from_attributes = True


class SystemLogIn(BaseModel):
    emp_id: UUID
    start_time: datetime


class SystemLogOut(BaseModel):
    emp_id: UUID
    end_time: datetime
