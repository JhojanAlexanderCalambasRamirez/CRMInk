from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    tattooer = "tattooer"
    client = "client"

class StudioBase(BaseModel):
    name: str
    description: str | None = None

class StudioResponse(StudioBase):
    id: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: UserRole = UserRole.client
    studio_id: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    studio_id: int
    is_active: bool
    class Config:
        orm_mode = True
