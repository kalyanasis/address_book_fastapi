from sqlalchemy.orm import Session
from app import models, schemas
import math

def create_address(db: Session, address: schemas.AddressCreate):
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()

def get_address(db: Session, address_id: int):
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def delete_address(db: Session, address_id: int):
    address = get_address(db, address_id)
    if address:
        db.delete(address)
        db.commit()
        return True
    return False

def update_address(db: Session, address_id: int, updated: schemas.AddressUpdate):
    address = get_address(db, address_id)
    if not address:
        return None
    for key, value in updated.dict().items():
        setattr(address, key, value)
    db.commit()
    db.refresh(address)
    return address

def get_addresses_within_radius(db: Session, latitude: float, longitude: float, distance_km: float):
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    all_addresses = db.query(models.Address).all()
    return [
        addr for addr in all_addresses
        if haversine(latitude, longitude, addr.latitude, addr.longitude) <= distance_km
    ]
