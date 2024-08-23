from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, validator

from app.database import models


class ApplicationCreate(BaseModel):
    room_id: int
    plan_id: int
    start_date: date

    @validator("start_date")
    def validate_start_date(cls, value):
        if value <= datetime.now().date():
            raise ValueError("Start date must be in the future")

        return value


class ApplicationUpdate(BaseModel):
    plan_id: Optional[int]
    start_date: Optional[date]

    @validator("start_date")
    def validate_start_date(cls, value):
        if value <= datetime.now().date():
            raise ValueError("Start date must be in the future")

        return value


class ApplicationPlan(BaseModel):
    id: int
    code: str
    duration: int
    fee: float
    discount: float

    class Config:
        from_attributes = True


class ApplicationRoom(BaseModel):
    id: int
    name: str
    monthly_price: float

    class Config:
        from_attributes = True


class Application(BaseModel):
    id: int
    room: ApplicationRoom
    plan: ApplicationPlan
    status: models.ApplicationStatus
    start_date: date
    monthly_price: float
    monthly_fee: float
    monthly_discount: float

    class Config:
        from_attributes = True
