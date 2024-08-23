from datetime import datetime
from typing import TYPE_CHECKING, cast

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import settings
from app.database import Base

if TYPE_CHECKING:
    from .plan import Plan
    from .apartment import Apartment, ApartmentRule
    from .application import Application
    from .building import Building
    from .subscription import Subscription


class Room(Base):
    __tablename__ = "room"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartment.id"))
    monthly_price: Mapped[float]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_available: Mapped[bool] = mapped_column(default=True)
    available_at: Mapped[datetime] = mapped_column(server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    apartment: Mapped["Apartment"] = relationship(
        back_populates="rooms",
    )
    building: Mapped["Building"] = relationship(back_populates="rooms")
    applications: Mapped[list["Application"]] = relationship(back_populates="room")
    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="room")
    assets: Mapped[list["RoomAsset"]] = relationship(back_populates="room")

    @property
    def zone(self):
        return self.building.zone

    @property
    def rules(self):
        if not self.apartment:
            return cast('list[ApartmentRule]', [])
        return self.apartment.rules

    @property
    def plans(self):
        if not self.apartment:
            return cast('list[Plan]', [])
        return self.apartment.plans

    @property
    def location(self):
        return self.building.position
    
    @property
    def starting_price(self) -> float:
        from app.services.rooms import calculate_room_price
        if not self.plans:
            return self.monthly_price
        return min([calculate_room_price(self, plan) for plan in self.plans])


class RoomAsset(Base):
    __tablename__ = "room_asset"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    key: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    room: Mapped[Room] = relationship(back_populates="assets")

    @property
    def url(self):
        return f"{settings.ASSETS_URL}/{self.key}"
