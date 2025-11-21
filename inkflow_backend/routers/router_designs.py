from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from databases.dbconexion import get_db
from auth.dependencies import get_current_user

router = APIRouter()

# Datos de ejemplo para categorías
SAMPLE_CATEGORIES = [
    {"id": 1, "style_name": "Minimalista", "characteristics": "Líneas simples y diseños limpios"},
    {"id": 2, "style_name": "Realismo", "characteristics": "Detalle fotográfico y sombras"},
    {"id": 3, "style_name": "Acuarela", "characteristics": "Efectos de pintura y difuminados"},
    {"id": 4, "style_name": "Japonés", "characteristics": "Tradicional con líneas gruesas"},
]

@router.get("/categories")
def get_categories(current_user: dict = Depends(get_current_user)):
    return {"categories": SAMPLE_CATEGORIES}

@router.get("/match")
def match_designs(
    styles: List[str],
    max_budget: float,
    min_budget: float = 0,
    body_area: Optional[str] = None,
    max_time: Optional[int] = None,
    current_user: dict = Depends(get_current_user)
):
    # Lógica de matching de diseños (demo)
    matching_designs = [
        {
            "id": 1,
            "design_name": "Diseño Minimalista",
            "description": "Diseño elegante y simple",
            "style_tags": ["minimalista", "líneas"],
            "estimated_time_min": 60,
            "estimated_price_range": {"min": 80, "max": 150},
            "match_percentage": 85
        }
    ]
    
    return {
        "matching_criteria": {
            "styles": styles,
            "budget_range": {"min": min_budget, "max": max_budget},
            "body_area": body_area,
            "max_time": max_time
        },
        "designs": matching_designs
    }
