from datetime import date
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    name: str
    email: str
    phone: str
    is_banned: bool
    is_completed: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str
    date_of_birth: date
