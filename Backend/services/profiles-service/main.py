from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.tattooer import router as tattooer_router
from routes.client import router as client_router
from routes.portfolio import router as portfolio_router
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Profiles Service iniciando...")
    await init_db()
    yield
    print("Profiles Service finalizando...")

app = FastAPI(title="Profiles Service", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tattooer_router, prefix="/api/tattooers", tags=["tattooers"])
app.include_router(client_router, prefix="/api/clients", tags=["clients"])
app.include_router(portfolio_router, prefix="/api/portfolio", tags=["portfolio"])

@app.get("/health")
async def health():
    return {"status": "Profiles Service OK"}