from sqlalchemy.orm import Session
from models.tattooer import Tattooer
from schemas.tattooer_schema import TattooerCreate, TattooerUpdate
from fastapi import HTTPException, status

class TattooerService:
    
    @staticmethod
    def create_tattooer(db: Session, user_id: int, studio_id: int, req: TattooerCreate):
        # Verificar que no exista ya un tatuador con este user_id
        existing = db.query(Tattooer).filter(Tattooer.user_id == user_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este usuario ya tiene un perfil de tatuador"
            )
        
        tattooer = Tattooer(
            user_id=user_id,
            studio_id=studio_id,
            display_name=req.display_name,
            bio=req.bio,
            styles=req.styles,
            hourly_rate=req.hourly_rate,
            profile_image_url=req.profile_image_url
        )
        db.add(tattooer)
        db.commit()
        db.refresh(tattooer)
        return tattooer
    
    @staticmethod
    def get_tattooer(db: Session, tattooer_id: int):
        tattooer = db.query(Tattooer).filter(Tattooer.id == tattooer_id).first()
        if not tattooer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tatuador no encontrado"
            )
        return tattooer
    
    @staticmethod
    def get_tattooers_by_studio(db: Session, studio_id: int):
        return db.query(Tattooer).filter(Tattooer.studio_id == studio_id).all()
    
    @staticmethod
    def update_tattooer(db: Session, tattooer_id: int, req: TattooerUpdate):
        tattooer = db.query(Tattooer).filter(Tattooer.id == tattooer_id).first()
        if not tattooer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tatuador no encontrado"
            )
        
        update_data = req.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tattooer, field, value)
        
        db.add(tattooer)
        db.commit()
        db.refresh(tattooer)
        return tattooer
    
    @staticmethod
    def delete_tattooer(db: Session, tattooer_id: int):
        tattooer = db.query(Tattooer).filter(Tattooer.id == tattooer_id).first()
        if not tattooer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tatuador no encontrado"
            )
        db.delete(tattooer)
        db.commit()
        return {"message": "Tatuador eliminado"}