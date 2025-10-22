import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:qChOZsjiSUKmzZoIIPjgYZtJnxsqZPtm@shinkansen.proxy.rlwy.net:33705/railway")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "inkflow-super-secret-key-change-in-production-2024")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()
