from datetime import date

from pydantic import BaseModel

from app.database import models


class SubscriptionCreate(BaseModel):
    room_id: int
    plan_id: int
    starts_at: date


class SubscriptionRoom(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SubscriptionPlan(BaseModel):
    id: int
    code: str
    duration: int
    fee: float

    class Config:
        from_attributes = True


class Subscription(BaseModel):
    id: int
    room: SubscriptionRoom
    plan: SubscriptionPlan
    starts_at: date
    ends_at: date
    amount: float
    status: models.SubscriptionStatus

    class Config:
        from_attributes = True
