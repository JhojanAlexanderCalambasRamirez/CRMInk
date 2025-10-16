from sqlalchemy.orm import Session
from models.portfolio import PortfolioImage
from schemas.portfolio_schema import PortfolioImageCreate
from fastapi import HTTPException, status

class PortfolioService:
    
    @staticmethod
    def add_image(db: Session, tattooer_id: int, studio_id: int, req: PortfolioImageCreate):
        image = PortfolioImage(
            tattooer_id=tattooer_id,
            studio_id=studio_id,
            image_url=req.image_url,
            style_tags=req.style_tags,
            body_area=req.body_area,
            size_label=req.size_label
        )
        db.add(image)
        db.commit()
        db.refresh(image)
        return image
    
    @staticmethod
    def get_portfolio_by_tattooer(db: Session, tattooer_id: int):
        return db.query(PortfolioImage).filter(PortfolioImage.tattooer_id == tattooer_id).all()
    
    @staticmethod
    def get_image(db: Session, image_id: int):
        image = db.query(PortfolioImage).filter(PortfolioImage.id == image_id).first()
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Imagen no encontrada"
            )
        return image
    
    @staticmethod
    def delete_image(db: Session, image_id: int):
        image = db.query(PortfolioImage).filter(PortfolioImage.id == image_id).first()
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Imagen no encontrada"
            )
        db.delete(image)
        db.commit()
        return {"message": "Imagen eliminada"}