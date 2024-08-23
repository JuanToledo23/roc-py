from pydantic import BaseModel

from app.database.models import PreferenceType


class Preference(BaseModel):
    id: int
    name: str
    is_selected: bool


class PreferenceUpdate(BaseModel):
    ids: list[int]
    type: PreferenceType
