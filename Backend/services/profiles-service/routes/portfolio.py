from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.portfolio_schema import PortfolioImageCreate, PortfolioImageResponse
from service.portfolio_service import PortfolioService
from service.tattooer_service import TattooerService
from utils.security import get_current_user

router = APIRouter()

@router.post("/{tattooer_id}/images", response_model=PortfolioImageResponse)
async def add_portfolio_image(
    tattooer_id: int,
    req: PortfolioImageCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tattooer = TattooerService.get_tattooer(db, tattooer_id)
    if tattooer.user_id != current_user["user_id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para agregar imágenes a este portafolio"
        )
    return PortfolioService.add_image(db, tattooer_id, current_user["studio_id"], req)

@router.get("/{tattooer_id}/images")
async def get_tattooer_portfolio(tattooer_id: int, db: Session = Depends(get_db)):
    return PortfolioService.get_portfolio_by_tattooer(db, tattooer_id)

@router.get("/images/{image_id}", response_model=PortfolioImageResponse)
async def get_portfolio_image(image_id: int, db: Session = Depends(get_db)):
    return PortfolioService.get_image(db, image_id)

@router.delete("/images/{image_id}")
async def delete_portfolio_image(
    image_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    image = PortfolioService.get_image(db, image_id)
    tattooer = TattooerService.get_tattooer(db, image.tattooer_id)
    if tattooer.user_id != current_user["user_id"] and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta imagen"
        )
    return PortfolioService.delete_image(db, image_id)