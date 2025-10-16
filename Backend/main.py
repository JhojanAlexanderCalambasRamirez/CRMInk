from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.profiles.routes import router as profiles_router
from app.scheduler.routes import router as scheduler_router

app = FastAPI(title="InkFlow API", version="1.0")

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(profiles_router, prefix="/api/profiles", tags=["Profiles"])
app.include_router(scheduler_router, prefix="/api/scheduler", tags=["Scheduler"])

@app.get("/")
def root():
    return {"message": "InkFlow API running"}
