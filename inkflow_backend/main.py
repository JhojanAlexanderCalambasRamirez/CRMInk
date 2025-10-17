from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.router_auth import router as router_auth
from routers.router_clients import router as router_clients
from routers.router_appointments import router as router_appointments
from routers.router_portfolio import router as router_portfolio
from routers.router_designs import router as router_designs
from routers.router_ai import router as router_ai
from routers.router_bot import router as router_bot

app = FastAPI(
    title="InkFlow CRM API",
    description="API para el sistema CRM especializado en tatuajes",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router_auth, prefix="/api/auth", tags=["Authentication"])
app.include_router(router_clients, prefix="/api/clients", tags=["Clients"])
app.include_router(router_appointments, prefix="/api/appointments", tags=["Appointments"])
app.include_router(router_portfolio, prefix="/api/portfolio", tags=["Portfolio"])
app.include_router(router_designs, prefix="/api/designs", tags=["Designs"])
app.include_router(router_ai, prefix="/api/ai", tags=["AI"])
app.include_router(router_bot, prefix="/api/bot", tags=["Bot"])

@app.get("/")
def root():
    return {"message": "🎨 InkFlow CRM API", "status": "active"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
