from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY, ForeignKey
from sqlalchemy.sql import func
from database import Base

class PortfolioImage(Base):
    __tablename__ = "portfolio_images"
    __table_args__ = {"schema": "inkflow"}

    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("inkflow.studios.id", ondelete="CASCADE"), nullable=False)
    tattooer_id = Column(Integer, ForeignKey("inkflow.tattooers.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(Text, nullable=False)
    style_tags = Column(ARRAY(String), default=[])
    body_area = Column(String(50))  
    size_label = Column(String(50))  
    uploaded_at = Column(DateTime, server_default=func.now())