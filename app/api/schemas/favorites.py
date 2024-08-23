from pydantic import BaseModel

from .zones import Zone


class BuildingFavorite(BaseModel):
    building_id: int


class RoomFavorite(BaseModel):
    room_id: int


class ZoneFavorite(Zone):
    is_selected: bool
