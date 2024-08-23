from datetime import datetime
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry, WKBElement
from geoalchemy2.shape import to_shape
from sqlalchemy import ForeignKey, func, select
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from app import settings
from app.database import Base
from .room import Room

if TYPE_CHECKING:
    from .apartment import Apartment
    from .zone import Zone


class Building(Base):
    __tablename__ = "building"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    zone_id: Mapped[int] = mapped_column(ForeignKey("zone.id"))
    address: Mapped[str]
    location: Mapped[WKBElement] = mapped_column(Geometry("POINT"))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    starting_price: Mapped[float] = column_property(
        select(func.coalesce(func.min(Room.monthly_price), 0).label("starting_price"))
        .where(Room.building_id == id)
        .scalar_subquery()
    )

    zone: Mapped["Zone"] = relationship(back_populates="buildings")
    amenities: Mapped[list["BuildingAmenity"]] = relationship(back_populates="building")
    rooms: Mapped[list["Room"]] = relationship(back_populates="building")
    apartments: Mapped[list["Apartment"]] = relationship(back_populates="building")
    assets: Mapped[list["BuildingAsset"]] = relationship(back_populates="building")

    @property
    def position(self) -> dict[str, float]:
        point = to_shape(self.location)

        return {
            "latitude": point.x,
            "longitude": point.y,
        }


class BuildingAmenity(Base):
    __tablename__ = "building_amenity"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))

    building: Mapped[Building] = relationship(back_populates="amenities")

    @property
    def url(self):
        return f"{settings.ASSETS_URL}/{self.key}"


class BuildingAsset(Base):
    __tablename__ = "building_asset"

    id: Mapped[int] = mapped_column(primary_key=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))
    key: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    building: Mapped[Building] = relationship(back_populates="assets")

    @property
    def url(self):
        return f"{settings.ASSETS_URL}/{self.key}"
