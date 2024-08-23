from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, tables

if TYPE_CHECKING:
    from app.database.models.building import Building
    from app.database.models.plan import Plan
    from app.database.models.room import Room


class Apartment(Base):
    __tablename__ = "apartment"

    id: Mapped[int] = mapped_column(primary_key=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))
    name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    building: Mapped["Building"] = relationship(back_populates="apartments")
    rooms: Mapped[list["Room"]] = relationship(back_populates="apartment")
    rules: Mapped[list["ApartmentRule"]] = relationship(back_populates="apartment")
    plans: Mapped[list["Plan"]] = relationship(secondary=tables.apartment_plan)


class ApartmentRule(Base):
    __tablename__ = "apartment_rule"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartment.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    apartment: Mapped["Apartment"] = relationship(back_populates="rules")
