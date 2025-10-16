from sqlalchemy.orm import Session
from models.user import User, UserRole
from models.studio import Studio
from schemas.auth_schema import RegisterRequest, LoginRequest
from utils.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status

class AuthService:
    
    @staticmethod
    def register(db: Session, req: RegisterRequest):
        # Verificar si el email ya existe
        existing_user = db.query(User).filter(User.email == req.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear studio (si es admin o tattooer)
        studio_id = None
        if req.role in ["admin", "tattooer"] and req.studio_name:
            studio = Studio(name=req.studio_name)
            db.add(studio)
            db.commit()
            db.refresh(studio)
            studio_id = studio.id
        
        # Crear usuario
        hashed_pw = hash_password(req.password)
        user = User(
            email=req.email,
            password_hash=hashed_pw,
            full_name=req.full_name,
            role=UserRole(req.role),
            studio_id=studio_id
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value
        }
    
    @staticmethod
    def login(db: Session, req: LoginRequest):
        user = db.query(User).filter(User.email == req.email).first()
        
        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña inválidos"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        token = create_access_token(
            email=user.email,
            user_id=user.id,
            role=user.role.value,
            studio_id=user.studio_id
        )
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value
            }
        }