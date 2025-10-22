from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from databases.dbconexion import engine, Base
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="InkFlow CRM API - Stable",
    description="API estable para el sistema CRM especializado en tatuajes",
    version="1.0.0"
)

# Middleware CORS simplificado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar routers de forma segura
try:
    from routers.router_auth import router as router_auth
    from routers.router_clients import router as router_clients
    from routers.router_appointments import router as router_appointments
    from routers.router_portfolio import router as router_portfolio
    from routers.router_designs import router as router_designs
    
    app.include_router(router_auth, prefix="/api/auth", tags=["Authentication"])
    app.include_router(router_clients, prefix="/api/clients", tags=["Clients"])
    app.include_router(router_appointments, prefix="/api/appointments", tags=["Appointments"])
    app.include_router(router_portfolio, prefix="/api/portfolio", tags=["Portfolio"])
    app.include_router(router_designs, prefix="/api/designs", tags=["Designs"])
    logger.info("✅ Todos los routers cargados correctamente")
    
except Exception as e:
    logger.warning(f"⚠️ Algunos routers no se cargaron: {e}")

# Cargar router de IA de forma condicional (puede fallar)
try:
    from routers.router_ai import router as router_ai
    from routers.router_bot import router as router_bot
    app.include_router(router_ai, prefix="/api/ai", tags=["AI"])
    app.include_router(router_bot, prefix="/api/bot", tags=["Bot"])
    logger.info("✅ Routers de IA cargados")
except Exception as e:
    logger.warning(f"⚠️ Routers de IA no disponibles: {e}")

@app.get("/")
def root():
    return {"message": "🎨 InkFlow CRM API - Stable", "status": "active"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/info")
def info():
    return {
        "name": "InkFlow CRM API",
        "version": "1.0.0",
        "status": "stable",
        "endpoints": [
            "/api/auth/*",
            "/api/clients/*", 
            "/api/appointments/*",
            "/api/portfolio/*",
            "/api/designs/*"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Iniciando servidor InkFlow estable...")
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=True)
