from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

# Enum para roles
class UserRole(enum.Enum):
    admin = "admin"
    tattooer = "tattooer"
    client = "client"

# Tabla de estudios
class Studio(Base):
    __tablename__ = "studios"
    __table_args__ = {"schema": "inkflow"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String)
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))

    users = relationship("User", back_populates="studio")

# Tabla de usuarios
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
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))

    studio = relationship("Studio", back_populates="users")
