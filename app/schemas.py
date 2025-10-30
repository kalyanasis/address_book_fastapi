from pydantic import BaseModel, Field
from typing import Optional

class AddressBase(BaseModel):
    name: str
    street: str
    city: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    pass

class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True
