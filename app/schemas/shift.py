from pydantic import BaseModel, Field, condecimal
from uuid import UUID
from datetime import time
from decimal import Decimal


class ShiftBase(BaseModel):
    name: str
    shift_code: str
    start_time: time
    end_time: time
    break_time: condecimal(ge=0, decimal_places=2)
    total_hours: condecimal(ge=0, decimal_places=2)
    half_day_shift_hours: condecimal(ge=0, decimal_places=2)
    late_coming_mins: condecimal(ge=0, decimal_places=2)
    early_going_mins: condecimal(ge=0, decimal_places=2)
    same_day: int  


class ShiftCreate(ShiftBase):  # ✅ Used in POST requests
    pass


class ShiftUpdate(BaseModel):  # ✅ Used in PUT requests
    name: str | None = None
    shift_code: str | None = None
    start_time: time | None = None
    end_time: time | None = None
    break_time: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    total_hours: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    half_day_shift_hours: Decimal | None = Field(
        default=None, ge=0, decimal_places=2)
    late_coming_mins: Decimal | None = Field(
        default=None, ge=0, decimal_places=2)
    early_going_mins: Decimal | None = Field(
        default=None, ge=0, decimal_places=2)
    same_day: int | None = None


class ShiftResponse(ShiftBase):  
    id: UUID

    class Config:
        from_attributes = True  # ✅ Ensures SQLAlchemy compatibility
