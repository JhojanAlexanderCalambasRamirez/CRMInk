from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

async def init_db():
    """Inicializar base de datos"""
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()