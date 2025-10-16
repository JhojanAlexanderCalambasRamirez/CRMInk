from sqlalchemy import Column, Integer, String, Time, TIMESTAMP, ForeignKey, Enum, CheckConstraint
from app.core.database import Base
import enum


class AppointmentStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class Availability(Base):
    __tablename__ = "availability"
    __table_args__ = {"schema": "inkflow"} 

    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("inkflow.studios.id", ondelete="CASCADE"))
    tattooer_id = Column(Integer, ForeignKey("inkflow.tattooers.id", ondelete="CASCADE"))
    weekday = Column(Integer)  
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    created_at = Column(TIMESTAMP, server_default="NOW()")


class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = {"schema": "inkflow"}  

    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("inkflow.studios.id", ondelete="CASCADE"))
    client_id = Column(Integer, ForeignKey("inkflow.clients.id", ondelete="CASCADE"))
    tattooer_id = Column(Integer, ForeignKey("inkflow.tattooers.id", ondelete="CASCADE"))
    starts_at = Column(TIMESTAMP, nullable=False)
    ends_at = Column(TIMESTAMP, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.pending)
    notes = Column(String)
    created_at = Column(TIMESTAMP, server_default="NOW()")
