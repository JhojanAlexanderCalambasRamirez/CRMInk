from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TATTOOER = "tattooer"
    CLIENT = "client"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "inkflow"}

    id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("inkflow.studios.id", ondelete="CASCADE"))
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENT, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())