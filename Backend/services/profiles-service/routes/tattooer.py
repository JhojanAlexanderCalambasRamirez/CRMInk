from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.tattooer_schema import TattooerCreate, TattooerUpdate, TattooerResponse
from service.tattooer_service import TattooerService
from utils.security import get_current_user

router = APIRouter()

@router.post("/", response_model=TattooerResponse)
async def create_tattooer(
    req: TattooerCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "tattooer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo tatuadores pueden crear este perfil"
        )
    return TattooerService.create_tattooer(db, current_user["user_id"], current_user["studio_id"], req)

@router.get("/{tattooer_id}", response_model=TattooerResponse)
async def get_tattooer(tattooer_id: int, db: Session = Depends(get_db)):
    return TattooerService.get_tattooer(db, tattooer_id)

@router.get("/studio/{studio_id}")
async def get_studio_tattooers(studio_id: int, db: Session = Depends(get_db)):
    return TattooerService.get_tattooers_by_studio(db, studio_id)

@router.put("/{tattooer_id}", response_model=TattooerResponse)
async def update_tattooer(
    tattooer_id: int,
    req: TattooerUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tattooer = TattooerService.get_tattooer(db, tattooer_id)
    if tattooer.user_id != current_user["user_id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar este perfil"
        )
    return TattooerService.update_tattooer(db, tattooer_id, req)

@router.delete("/{tattooer_id}")
async def delete_tattooer(
    tattooer_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tattooer = TattooerService.get_tattooer(db, tattooer_id)
    if tattooer.user_id != current_user["user_id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este perfil"
        )
    return TattooerService.delete_tattooer(db, tattooer_id)