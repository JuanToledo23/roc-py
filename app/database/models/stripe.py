from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from .user import User


class StripeCustomer(Base):
    __tablename__ = "stripe_customer"

    id: Mapped[str] = mapped_column(primary_key=True)
    profile_id: Mapped[UUID] = mapped_column(ForeignKey("profile.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="stripe_customers")


class StripeCard(Base):
    __tablename__ = 'stripe_card'

    id: Mapped[str] = mapped_column(primary_key=True)
    profile_id: Mapped[UUID] = mapped_column(ForeignKey('profile.id'))
    brand: Mapped[str]
    exp_month: Mapped[int]
    exp_year: Mapped[int]
    funding: Mapped[str]
    last4: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now())

    user: Mapped['User'] = relationship(back_populates='stripe_cards')
