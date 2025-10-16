from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.scheduler import models, schemas

router = APIRouter()  

@router.post("/availability", response_model=schemas.AvailabilityResponse)
def create_availability(data: schemas.AvailabilityCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Availability).filter_by(
        tattooer_id=data.tattooer_id,
        weekday=data.weekday,
        start_time=data.start_time,
        end_time=data.end_time
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="This availability slot already exists")

    availability = models.Availability(**data.dict())
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability



# === Obtener disponibilidades de un tatuador ===
@router.get("/availability/{tattooer_id}", response_model=list[schemas.AvailabilityResponse])
def get_availability_by_tattooer(tattooer_id: int, db: Session = Depends(get_db)):
    records = db.query(models.Availability).filter(models.Availability.tattooer_id == tattooer_id).all()
    if not records:
        raise HTTPException(status_code=404, detail="No availability found for this tattooer")
    return records
