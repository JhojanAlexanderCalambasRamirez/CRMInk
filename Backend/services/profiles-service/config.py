from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    DATABASE_URL: str
    
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    
    PROFILES_SERVICE_PORT: int = 8002
    
    AUTH_SERVICE_URL: str = "http://localhost:8001"
    SCHEDULER_SERVICE_URL: str = "http://localhost:8003"
    AI_BOT_SERVICE_URL: str = "http://localhost:8004"
    
    class Config:
        env_file = "/Backend/services/.env"

@lru_cache()
def get_settings():
    return Settings()