from pydantic import BaseModel
from typing import Optional, List

class TattooerCreate(BaseModel):
    display_name: str
    bio: Optional[str] = None
    styles: List[str] = []
    hourly_rate: float = 0.0
    profile_image_url: Optional[str] = None

class TattooerUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    styles: Optional[List[str]] = None
    hourly_rate: Optional[float] = None
    profile_image_url: Optional[str] = None

class TattooerResponse(BaseModel):
    id: int
    user_id: int
    display_name: str
    bio: Optional[str]
    styles: List[str]
    hourly_rate: float
    rating: float
    profile_image_url: Optional[str]

    class Config:
        from_attributes = True