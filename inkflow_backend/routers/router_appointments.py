from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from databases.dbconexion import get_db
from databases.schemas import Appointment, Availability
from schemas.models_base import AppointmentCreate, AppointmentResponse
from auth.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appointments = db.query(Appointment).offset(skip).limit(limit).all()
    return appointments

@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    appointment_data: AppointmentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verificar disponibilidad
    appointment = Appointment(**appointment_data.dict())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

@router.get("/availability/{tattooer_id}", response_model=List[dict])
def get_availability(
    tattooer_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    availability = db.query(Availability).filter(Availability.tattooer_id == tattooer_id).all()
    return availability
