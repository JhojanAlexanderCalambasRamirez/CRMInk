from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "client"
    studio_name: str = None

class RegisterResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class TokenPayload(BaseModel):
    sub: str
    role: str
    user_id: int
    studio_id: int
    exp: int