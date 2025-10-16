from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.profiles import models, schemas

router = APIRouter()

# === Crear perfil de tatuador ===
@router.post("/tattooer", response_model=schemas.TattooerResponse)
def create_tattooer_profile(data: schemas.TattooerCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Tattooer).filter_by(user_id=data.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tattooer profile already exists")

    tattooer = models.Tattooer(**data.dict())
    db.add(tattooer)
    db.commit()
    db.refresh(tattooer)
    return tattooer


# === Obtener perfil de tatuador por ID ===
@router.get("/tattooer/{user_id}", response_model=schemas.TattooerResponse)
def get_tattooer_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.Tattooer).filter_by(user_id=user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Tattooer profile not found")
    return profile


# === Crear cliente ===
@router.post("/clients", response_model=schemas.ClientResponse)
def create_client(data: schemas.ClientCreate, db: Session = Depends(get_db)):
    client = models.Client(**data.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


# === Listar clientes de un estudio ===
@router.get("/clients/{studio_id}", response_model=list[schemas.ClientResponse])
def list_clients(studio_id: int, db: Session = Depends(get_db)):
    clients = db.query(models.Client).filter(models.Client.studio_id == studio_id).all()
    return clients
