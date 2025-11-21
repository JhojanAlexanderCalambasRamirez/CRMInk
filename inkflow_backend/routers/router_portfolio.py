from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from databases.dbconexion import get_db
from databases.schemas import PortfolioImage
from schemas.models_base import PortfolioImageCreate, PortfolioImageResponse
from auth.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[PortfolioImageResponse])
def get_portfolio_images(
    tattooer_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    images = db.query(PortfolioImage).filter(
        PortfolioImage.tattooer_id == tattooer_id
    ).offset(skip).limit(limit).all()
    return images

@router.post("/", response_model=PortfolioImageResponse)
def create_portfolio_image(
    image_data: PortfolioImageCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    image = PortfolioImage(**image_data.dict())
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

@router.post("/upload")
def upload_portfolio_image(
    file: UploadFile = File(...),
    tattooer_id: int = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Demo de subida de imagen
    return {
        "filename": file.filename,
        "tattooer_id": tattooer_id,
        "message": "Image uploaded successfully (demo)"
    }
