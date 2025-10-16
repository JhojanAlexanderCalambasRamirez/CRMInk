from pydantic import BaseModel
from datetime import time, datetime
from enum import Enum

class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


# === Availability ===
class AvailabilityCreate(BaseModel):
    studio_id: int
    tattooer_id: int
    weekday: int
    start_time: time
    end_time: time


class AvailabilityResponse(AvailabilityCreate):
    id: int
    class Config:
        from_attributes = True


# === Appointment ===
class AppointmentCreate(BaseModel):
    studio_id: int
    client_id: int
    tattooer_id: int
    starts_at: datetime
    ends_at: datetime
    notes: str | None = None


class AppointmentResponse(AppointmentCreate):
    id: int
    status: AppointmentStatus
    class Config:
        from_attributes = True
