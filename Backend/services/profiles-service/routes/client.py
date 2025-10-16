from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.client_schema import ClientCreate, ClientUpdate, ClientResponse
from service.client_service import ClientService
from utils.security import get_current_user

router = APIRouter()

@router.post("/", response_model=ClientResponse)
async def create_client(
    req: ClientCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ClientService.create_client(db, current_user["studio_id"], req)

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    return ClientService.get_client(db, client_id)

@router.get("/studio/{studio_id}")
async def get_studio_clients(studio_id: int, db: Session = Depends(get_db)):
    return ClientService.get_clients_by_studio(db, studio_id)

@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    req: ClientUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ClientService.update_client(db, client_id, req)

@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return ClientService.delete_client(db, client_id)