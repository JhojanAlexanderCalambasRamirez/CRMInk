from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.scheduler import models, schemas

router = APIRouter()

# === Crear disponibilidad ===
@router.post("/availability", response_model=schemas.AvailabilityResponse)
def create_availability(data: schemas.AvailabilityCreate, db: Session = Depends(get_db)):
    availability = models.Availability(**data.dict())
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability


# === Crear cita (con validación de solape) ===
@router.post("/appointments", response_model=schemas.AppointmentResponse)
def create_appointment(data: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    conflict = db.query(models.Appointment).filter(
        models.Appointment.tattooer_id == data.tattooer_id,
        models.Appointment.status.in_(["pending", "confirmed"]),
        models.Appointment.starts_at < data.ends_at,
        models.Appointment.ends_at > data.starts_at
    ).first()

    if conflict:
        raise HTTPException(status_code=409, detail="Time slot already booked")

    appointment = models.Appointment(**data.dict())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


# === Listar citas por tatuador ===
@router.get("/appointments/tattooer/{tattooer_id}", response_model=list[schemas.AppointmentResponse])
def list_appointments_by_tattooer(tattooer_id: int, db: Session = Depends(get_db)):
    return db.query(models.Appointment).filter(models.Appointment.tattooer_id == tattooer_id).all()
