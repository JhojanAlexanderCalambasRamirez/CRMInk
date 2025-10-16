from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    DATABASE_URL: str
    
    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # Puertos
    AUTH_SERVICE_PORT: int = 8001
    
    # URLs de servicios
    PROFILES_SERVICE_URL: str = "http://localhost:8002"
    SCHEDULER_SERVICE_URL: str = "http://localhost:8003"
    AI_BOT_SERVICE_URL: str = "http://localhost:8004"
    
    class Config:
        env_file = "../.env"

@lru_cache()
def get_settings():
    return Settings()