from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime, time
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    tattooer = "tattooer"
    client = "client"

class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.client

class UserCreate(UserBase):
    password: str
    studio_id: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    studio_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Studio Schemas
class StudioBase(BaseModel):
    name: str
    description: Optional[str] = None

class StudioResponse(StudioBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Tattooer Schemas
class TattooerBase(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    styles: Optional[List[str]] = None
    hourly_rate: Optional[float] = None
    social_links: Optional[Dict[str, str]] = None
    profile_image_url: Optional[str] = None

class TattooerCreate(TattooerBase):
    studio_id: int
    user_id: int

class TattooerResponse(TattooerBase):
    id: int
    rating: float
    created_at: datetime

    class Config:
        from_attributes = True

# Client Schemas
class ClientBase(BaseModel):
    full_name: str
    phone: Optional[str] = None
    instagram: Optional[str] = None
    notes: Optional[str] = None
    preferred_styles: Optional[List[str]] = None

class ClientCreate(ClientBase):
    studio_id: int

class ClientResponse(ClientBase):
    id: int
    studio_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Appointment Schemas
class AppointmentBase(BaseModel):
    client_id: int
    tattooer_id: int
    starts_at: datetime
    ends_at: datetime
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    studio_id: int

class AppointmentResponse(AppointmentBase):
    id: int
    studio_id: int
    status: AppointmentStatus
    created_at: datetime

    class Config:
        from_attributes = True

# Availability Schemas
class AvailabilityBase(BaseModel):
    tattooer_id: int
    weekday: int
    start_time: time
    end_time: time

class AvailabilityCreate(AvailabilityBase):
    studio_id: int

class AvailabilityResponse(AvailabilityBase):
    id: int
    studio_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Portfolio Image Schemas
class PortfolioImageBase(BaseModel):
    image_url: str
    style_tags: Optional[List[str]] = None
    body_area: Optional[str] = None
    size_label: Optional[str] = None

class PortfolioImageCreate(PortfolioImageBase):
    studio_id: int
    tattooer_id: int

class PortfolioImageResponse(PortfolioImageBase):
    id: int
    studio_id: int
    tattooer_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True
