from sqlalchemy.orm import Session
from models.client import Client
from schemas.client_schema import ClientCreate, ClientUpdate
from fastapi import HTTPException, status

class ClientService:
    
    @staticmethod
    def create_client(db: Session, studio_id: int, req: ClientCreate):
        client = Client(
            studio_id=studio_id,
            full_name=req.full_name,
            phone=req.phone,
            instagram=req.instagram,
            preferred_styles=req.preferred_styles
        )
        db.add(client)
        db.commit()
        db.refresh(client)
        return client
    
    @staticmethod
    def get_client(db: Session, client_id: int):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        return client
    
    @staticmethod
    def get_clients_by_studio(db: Session, studio_id: int):
        return db.query(Client).filter(Client.studio_id == studio_id).all()
    
    @staticmethod
    def update_client(db: Session, client_id: int, req: ClientUpdate):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        update_data = req.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client, field, value)
        
        db.add(client)
        db.commit()
        db.refresh(client)
        return client
    
    @staticmethod
    def delete_client(db: Session, client_id: int):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        db.delete(client)
        db.commit()
        return {"message": "Cliente eliminado"}