from pydantic import BaseModel

class StatsResponse(BaseModel):
    employee_count: int
    department_count: int
    shift_count: int
    designation_count: int
    project_count: int