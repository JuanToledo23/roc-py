from datetime import date

from pydantic import BaseModel

from app.database import models


class PersonalInformationCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: models.Gender


class PersonalInformation(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: models.Gender

    class Config:
        from_attributes = True
