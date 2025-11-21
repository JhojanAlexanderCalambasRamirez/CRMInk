from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from databases.dbconexion import get_db
from auth.dependencies import get_current_user

router = APIRouter()

@router.post("/session")
def create_bot_session(
    client_phone: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Demo de sesión de bot
    return {
        "session_id": "demo_session_123",
        "client_phone": client_phone,
        "current_state": "greeting",
        "message": "Bot session created successfully"
    }

@router.post("/process")
def process_bot_message(
    message: str,
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Demo de procesamiento de mensaje
    responses = {
        "hola": "¡Hola! ¿Buscas hacerte un tatuaje?",
        "precio": "Los precios varían según el diseño y tamaño. ¿Qué estilo te interesa?",
        "minimalista": "Tenemos excelentes artistas de estilo minimalista. ¿Quieres ver algunos diseños?",
        "disponibilidad": "Puedo ayudarte a encontrar disponibilidad. ¿Qué días tienes libre?"
    }
    
    response = responses.get(message.lower(), "No entendí tu mensaje. ¿Puedes reformularlo?")
    
    return {
        "session_id": session_id,
        "user_message": message,
        "bot_response": response,
        "next_state": "waiting_response"
    }
