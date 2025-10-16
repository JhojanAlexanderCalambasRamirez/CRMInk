from pydantic import BaseModel
from typing import Optional, List

class PortfolioImageCreate(BaseModel):
    image_url: str
    style_tags: List[str] = []
    body_area: Optional[str] = None
    size_label: Optional[str] = None

class PortfolioImageResponse(BaseModel):
    id: int
    tattooer_id: int
    image_url: str
    style_tags: List[str]
    body_area: Optional[str]
    size_label: Optional[str]

    class Config:
        from_attributes = True