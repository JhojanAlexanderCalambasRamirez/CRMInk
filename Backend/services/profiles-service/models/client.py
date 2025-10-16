from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Client(Base):
    __tablename__ = "clients"
    __table_args__ = {"schema": "inkflow"}

    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("inkflow.studios.id", ondelete="CASCADE"), nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(30))
    instagram = Column(String(100))
    notes = Column(Text)
    preferred_styles = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, server_default=func.now())