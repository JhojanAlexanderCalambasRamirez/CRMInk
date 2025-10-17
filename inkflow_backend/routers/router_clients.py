from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from databases.dbconexion import get_db
from databases.schemas import Client
from schemas.models_base import ClientCreate, ClientResponse
from auth.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ClientResponse])
def get_clients(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    clients = db.query(Client).offset(skip).limit(limit).all()
    return clients

@router.post("/", response_model=ClientResponse)
def create_client(
    client_data: ClientCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    client = Client(**client_data.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client
