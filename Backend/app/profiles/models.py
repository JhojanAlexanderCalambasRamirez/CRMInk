from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Numeric, JSON, ARRAY, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base

class Tattooer(Base):
    __tablename__ = "tattooers"
    __table_args__ = {"schema": "inkflow"}

    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("inkflow.studios.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("inkflow.users.id", ondelete="CASCADE"), unique=True)
    display_name = Column(String(100))
    bio = Column(Text)
    styles = Column(ARRAY(String))
    hourly_rate = Column(Numeric(10, 2))
    social_links = Column(JSON)
    profile_image_url = Column(Text)
    rating = Column(Numeric(2, 1), default=0.0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Client(Base):
    __tablename__ = "clients"
    __table_args__ = {"schema": "inkflow"}

    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("inkflow.studios.id", ondelete="CASCADE"))
    full_name = Column(String(100), nullable=False)
    phone = Column(String(30))
    instagram = Column(String(100))
    notes = Column(Text)
    preferred_styles = Column(ARRAY(String))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
