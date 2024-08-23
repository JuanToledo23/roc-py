from datetime import datetime
from typing import TYPE_CHECKING, List

from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import settings
from app.database import Base

if TYPE_CHECKING:
    from app.database.models.building import Building


class Zone(Base):
    __tablename__ = "zone"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    buildings: Mapped[List["Building"]] = relationship(back_populates="zone")
    assets: Mapped[list["ZoneAsset"]] = relationship(back_populates="zone")
    places: Mapped[list["ZonePlace"]] = relationship(back_populates="zone")

    def __repr__(self) -> str:
        return f"Zone(id={self.id}, name={self.name}, is_active={self.is_active})"


class ZonePlace(Base):
    __tablename__ = "zone_place"

    id: Mapped[int] = mapped_column(primary_key=True)
    zone_id: Mapped[int] = mapped_column(ForeignKey("zone.id"))
    name: Mapped[str]
    description: Mapped[str]
    location: Mapped[WKBElement] = mapped_column(Geometry("POINT"))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    zone: Mapped["Zone"] = relationship(back_populates="places")


class ZoneAsset(Base):
    __tablename__ = "zone_asset"

    id: Mapped[int] = mapped_column(primary_key=True)
    zone_id: Mapped[int] = mapped_column(ForeignKey("zone.id"))
    key: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    zone: Mapped["Zone"] = relationship(back_populates="assets")

    @property
    def url(self):
        return f"{settings.ASSETS_URL}/{self.key}"
