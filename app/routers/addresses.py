from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/addresses", tags=["Addresses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    return crud.create_address(db, address)

@router.get("/", response_model=list[schemas.Address])
def get_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_addresses(db, skip, limit)

@router.get("/{address_id}", response_model=schemas.Address)
def get_address(address_id: int, db: Session = Depends(get_db)):
    address = crud.get_address(db, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.put("/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, updated: schemas.AddressUpdate, db: Session = Depends(get_db)):
    address = crud.update_address(db, address_id, updated)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    success = crud.delete_address(db, address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"ok": True}

@router.get("/within-radius/", response_model=list[schemas.Address])
def get_addresses_within_radius(latitude: float, longitude: float, distance_km: float, db: Session = Depends(get_db)):
    return crud.get_addresses_within_radius(db, latitude, longitude, distance_km)
