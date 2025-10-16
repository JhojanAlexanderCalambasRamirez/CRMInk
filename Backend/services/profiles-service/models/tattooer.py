from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ARRAY, JSON, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Tattooer(Base):
    __tablename__ = "tattooers"
    __table_args__ = {"schema": "inkflow"}

    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("inkflow.studios.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("inkflow.users.id", ondelete="CASCADE"), unique=True, nullable=False)
    display_name = Column(String(100))
    bio = Column(Text)
    styles = Column(ARRAY(String), default=[]) 
    hourly_rate = Column(Float, default=0.0)
    social_links = Column(JSON, default={})  
    profile_image_url = Column(Text)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())