from datetime import date, datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SubscriptionStatus(Enum):
    active = "active"
    inactive = "inactive"
    cancelled = "cancelled"


class Subscription(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    plan_id: Mapped[int] = mapped_column(ForeignKey("plan.id"))
    starts_at: Mapped[date]
    ends_at: Mapped[date]
    amount: Mapped[float]
    status: Mapped[SubscriptionStatus] = mapped_column(
        default=SubscriptionStatus.active
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="subscriptions")
    room: Mapped["Room"] = relationship(back_populates="subscriptions")
    plan: Mapped["Plan"] = relationship(back_populates="subscriptions")

    payments: Mapped[list["SubscriptionPayment"]] = relationship(
        back_populates="subscription"
    )


class SubscriptionPayment(Base):
    __tablename__ = "subscription_payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscription.id"))
    payment_method_id: Mapped[int] = mapped_column(ForeignKey("payment_method.id"))
    amount: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    subscription: Mapped["Subscription"] = relationship(back_populates="payments")
    payment_method: Mapped["PaymentMethod"] = relationship(
        back_populates="subscription_payments"
    )
