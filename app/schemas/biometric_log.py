from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

from app.schemas.employee import EmployeeResponse


class BiometricLogBase(BaseModel):
    emp_id: UUID4
    employee: EmployeeResponse
    in_time: Optional[datetime] = None
    out_time: Optional[datetime] = None


class BiometricLogCreate(BiometricLogBase):
    pass


class BiometricLogUpdate(BaseModel):
    in_time: Optional[datetime] = None
    out_time: Optional[datetime] = None


class BiometricLogResponse(BiometricLogBase):
    id: UUID4

    class Config:
        from_attributes = True