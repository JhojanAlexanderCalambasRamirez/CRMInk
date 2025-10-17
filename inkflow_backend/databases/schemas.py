from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, TIMESTAMP, Text, ARRAY, JSON, Numeric, Time
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM
from .dbconexion import Base
import enum

class UserRole(enum.Enum):
    admin = "admin"
    tattooer = "tattooer"
    client = "client"

class AppointmentStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class Studio(Base):
    __tablename__ = "studios"
    __table_args__ = {"schema": "inkflow"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "inkflow"}

    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("inkflow.studios.id", ondelete="CASCADE"))
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.client)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

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
    created_at = Column(TIMESTAMP, server_default=func.now())

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
    created_at = Column(TIMESTAMP, server_default=func.now())

class Availability(Base):
    __tablename__ = "availability"
    __table_args__ = {"schema": "inkflow"}

    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("inkflow.studios.id", ondelete="CASCADE"))
    tattooer_id = Column(Integer, ForeignKey("inkflow.tattooers.id", ondelete="CASCADE"))
    weekday = Column(Integer)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

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
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

class PortfolioImage(Base):
    __tablename__ = "portfolio_images"
    __table_args__ = {"schema": "inkflow"}

    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("inkflow.studios.id", ondelete="CASCADE"))
    tattooer_id = Column(Integer, ForeignKey("inkflow.tattooers.id", ondelete="CASCADE"))
    image_url = Column(Text, nullable=False)
    style_tags = Column(ARRAY(String))
    body_area = Column(String(50))
    size_label = Column(String(50))
    uploaded_at = Column(TIMESTAMP, server_default=func.now())
