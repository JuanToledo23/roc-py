from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel

from .location import Location


class RoomZone(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RoomRule(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class RoomBuilding(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        from_attributes = True


class RoomAsset(BaseModel):
    id: int
    url: str

    class Config:
        from_attributes = True


class Room(BaseModel):
    id: int
    name: str
    description: str
    building: RoomBuilding
    zone: RoomZone
    monthly_price: float
    is_available: bool
    available_at: Optional[datetime]
    assets: list[RoomAsset]
    rules: list[RoomRule]
    location: Location
    starting_price: float

    class Config:
        from_attributes = True


class RoomCalendar(BaseModel):
    since: date
    available_at: list[date]


class RoomPlan(BaseModel):
    id: int
    code: str
    duration: int
    monthly_price: float
    discount: float
