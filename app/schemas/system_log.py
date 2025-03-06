from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from app.schemas.employee import EmployeeResponse


class SystemLogResponse(BaseModel):
    id: UUID
    employee: EmployeeResponse
    in_ip_address: str | None
    out_ip_address: str | None
    start_time: datetime | None
    end_time: datetime | None

    class Config:
        from_attributes = True


class SystemLogIn(BaseModel):
    emp_id: UUID
    ip_address: str
    start_time: datetime


class SystemLogOut(BaseModel):
    emp_id: UUID
    ip_address: str
    end_time: datetime
