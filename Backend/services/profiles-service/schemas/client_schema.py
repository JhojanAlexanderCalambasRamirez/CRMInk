from pydantic import BaseModel
from typing import Optional, List

class ClientCreate(BaseModel):
    full_name: str
    phone: Optional[str] = None
    instagram: Optional[str] = None
    preferred_styles: List[str] = []

class ClientUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    instagram: Optional[str] = None
    notes: Optional[str] = None
    preferred_styles: Optional[List[str]] = None

class ClientResponse(BaseModel):
    id: int
    full_name: str
    phone: Optional[str]
    instagram: Optional[str]
    preferred_styles: List[str]

    class Config:
        from_attributes = True