from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.auth import router as auth_router
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Auth Service iniciando...")
    await init_db()
    yield
    print("Auth Service finalizando...")

app = FastAPI(title="Auth Service", version="1.0.0", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

@app.get("/health")
async def health():
    return {"status": "Auth Service OK"}