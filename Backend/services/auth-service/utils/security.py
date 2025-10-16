from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt
from config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(email: str, user_id: int, role: str, studio_id: int, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": email,
        "user_id": user_id,
        "role": role,
        "studio_id": studio_id,
        "exp": expire
    }
    
    encoded_jwt = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")