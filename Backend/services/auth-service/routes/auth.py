from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.auth_schema import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from services.auth_service import AuthService
from utils.decorators import get_current_user

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService.register(db, req)

@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.login(db, req)

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["user_id"],
        "email": current_user["sub"],
        "role": current_user["role"],
        "studio_id": current_user["studio_id"]
    }

@router.get("/verify")
async def verify_token(current_user: dict = Depends(get_current_user)):
    return {"valid": True, "user": current_user}