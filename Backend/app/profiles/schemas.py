from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

# === Tattooer Schemas ===
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

# === Client Schemas ===
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
