from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class PricingRule(Base):
    __tablename__ = "pricing_rules"
    __table_args__ = {"schema": "inkflow"}

    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("inkflow.studios.id", ondelete="CASCADE"), nullable=False)
    tattooer_id = Column(Integer, ForeignKey("inkflow.tattooers.id", ondelete="CASCADE"), nullable=False)
    base_price = Column(Float, default=0.0)
    per_cm2 = Column(Float, default=0.0)
    min_price = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())