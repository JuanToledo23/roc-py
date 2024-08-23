import enum
from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from .user import User


class Gender(str, enum.Enum):
    MALE = "M"
    FEMALE = "F"


class PersonalInformation(Base):
    __tablename__ = "personal_information"

    profile_id: Mapped[UUID] = mapped_column(ForeignKey("profile.id"), primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    gender: Mapped[Gender] = mapped_column(
        Enum(Gender, values_callable=lambda obj: [e.value for e in obj])
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="personal_information")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
