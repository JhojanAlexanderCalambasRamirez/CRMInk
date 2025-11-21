from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from databases.dbconexion import get_db
from services import ai_service
from pydantic import BaseModel

router = APIRouter(tags=["AI"])

@router.get("/analyze_tattooers/{studio_id}")
def analyze_tattooers(studio_id: int, db: Session = Depends(get_db)):
    return ai_service.analyze_tattooers(db, studio_id)

@router.get("/analyze_clients/{studio_id}")
def analyze_clients(studio_id: int, db: Session = Depends(get_db)):
    return ai_service.analyze_clients(db, studio_id)

@router.post("/label_image")
async def label_image(
    studio_id: int = Form(...),
    tattooer_id: int = Form(...),
    style_preference: str = Form(...),
    color_scheme: str = Form(...),
    body_area: str = Form(...),
    size_label: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return await ai_service.label_image_binary(
        db, tattooer_id, studio_id, image, style_preference, color_scheme, body_area, size_label
    )

class IdeaRequest(BaseModel):
    style: str
    color: str

@router.post("/recommend_idea")
def recommend_idea(data: IdeaRequest, db: Session = Depends(get_db)):
    try:
        return ai_service.recommend_idea(db, data.style, data.color)
    except Exception as e:
        # Fallback seguro si hay algún error
        return {
            "idea": f"💡 Idea demo para {data.style} en {data.color}: Diseño creativo que combina elementos del estilo solicitado. Zona recomendada: brazo. Tamaño: mediano. [Sistema en modo demo]"
        }
