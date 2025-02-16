from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class AttendanceIn(BaseModel):
    emp_id: UUID
    start_time: datetime

class AttendanceOut(BaseModel):
    emp_id: UUID
    end_time: datetime