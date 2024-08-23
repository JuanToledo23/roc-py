from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ApplicationStatus(Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class Application(Base):
    __tablename__ = "application"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[UUID] = mapped_column(ForeignKey("profile.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    plan_id: Mapped[int] = mapped_column(ForeignKey("plan.id"))
    start_date: Mapped[date]
    status: Mapped[ApplicationStatus] = mapped_column(default=ApplicationStatus.pending)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())
    approved_at: Mapped[Optional[datetime]]
    rejected_at: Mapped[Optional[datetime]]
    rejected_reason: Mapped[Optional[str]]

    profile: Mapped["User"] = relationship(
        back_populates="applications",
    )

    room: Mapped["Room"] = relationship(
        back_populates="applications",
    )

    plan: Mapped["Plan"] = relationship(
        back_populates="applications",
    )

    events: Mapped[list["ApplicationEvent"]] = relationship(
        back_populates="application"
    )

    @property
    def monthly_price(self):
        return self.room.monthly_price + self.monthly_fee

    @property
    def monthly_fee(self):
        return self.plan.fee * self.room.monthly_price

    @property
    def monthly_discount(self):
        return 0.0


class ApplicationEvent(Base):
    __tablename__ = "application_event"

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("application.id"))
    name: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    application: Mapped["Application"] = relationship(
        back_populates="events",
    )
