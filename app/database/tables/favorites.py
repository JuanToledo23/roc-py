from sqlalchemy import Column, ForeignKey, Table

from app.database import Base

room_favorite = Table(
    "room_favorite",
    Base.metadata,
    Column("profile_id", ForeignKey("profile.id")),
    Column("room_id", ForeignKey("room.id")),
)

building_favorite = Table(
    "building_favorite",
    Base.metadata,
    Column("profile_id", ForeignKey("profile.id")),
    Column("building_id", ForeignKey("building.id")),
)

zone_favorite = Table(
    "zone_favorite",
    Base.metadata,
    Column("profile_id", ForeignKey("profile.id")),
    Column("zone_id", ForeignKey("zone.id")),
)
