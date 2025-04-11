from pydantic import BaseModel


class AllocationStatusUpdateRequest(BaseModel):
    status: str