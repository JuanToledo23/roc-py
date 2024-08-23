from datetime import datetime, date
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from ..tables import favorites, preferences

if TYPE_CHECKING:
    from .application import Application
    from .building import Building
    from .payment_method import PaymentMethod
    from .personal_information import PersonalInformation
    from .preferences import Preference
    from .room import Room
    from .stripe import StripeCustomer, StripeCard
    from .subscription import Subscription
    from .zone import Zone
    from.veriff import VeriffVerification, VeriffSession


class User(Base):
    __tablename__ = "profile"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(default="")
    email: Mapped[str]
    phone: Mapped[str]
    date_of_birth: Mapped[date]
    is_completed: Mapped[bool] = mapped_column(default=False)
    is_banned: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    personal_information: Mapped["PersonalInformation"] = relationship(
        back_populates="user"
    )

    applications: Mapped[list["Application"]] = relationship(back_populates="profile")

    # Favorites

    zone_favorites: Mapped[list["Zone"]] = relationship(
        secondary=favorites.zone_favorite
    )

    building_favorites: Mapped[list["Building"]] = relationship(
        secondary=favorites.building_favorite
    )

    room_favorites: Mapped[list["Room"]] = relationship(
        secondary=favorites.room_favorite
    )

    preferences: Mapped[list["Preference"]] = relationship(
        secondary=preferences.user_preference
    )

    payment_methods: Mapped[list["PaymentMethod"]] = relationship(back_populates="user")

    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="user")

    stripe_customers: Mapped[list["StripeCustomer"]] = relationship(
        back_populates="user"
    )

    stripe_cards: Mapped[list["StripeCard"]] = relationship(back_populates="user")

    veriff_verifications: Mapped[list["VeriffVerification"]] = relationship(back_populates="profile")

    veriff_sessions: Mapped[list["VeriffSession"]] = relationship(back_populates="profile")

    @property
    def full_name(self) -> str:
        if self.personal_information is None:
            return ""

        return self.personal_information.full_name
