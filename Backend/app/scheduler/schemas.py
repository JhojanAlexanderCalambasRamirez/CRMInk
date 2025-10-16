from pydantic import BaseModel
from datetime import time, datetime


class AvailabilityBase(BaseModel):
    studio_id: int
    tattooer_id: int
    weekday: int
    start_time: time
    end_time: time


class AvailabilityCreate(AvailabilityBase):
    pass


class AvailabilityResponse(AvailabilityBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
