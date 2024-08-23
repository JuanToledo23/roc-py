from datetime import date, datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import ForeignKey, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from .user import User


class VeriffSession(Base):
    __tablename__ = "veriff_session"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    profile_id: Mapped[UUID] = mapped_column(ForeignKey("profile.id"))

    url: Mapped[str]
    status: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    profile: Mapped["User"] = relationship(back_populates="veriff_sessions")


class VeriffVerification(Base):
    __tablename__ = "veriff_verification"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    profile_id: Mapped[UUID] = mapped_column(ForeignKey("profile.id"))

    decision: Mapped[str]
    response: Mapped[dict[Any, Any]] = mapped_column(JSON)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    profile: Mapped["User"] = relationship(back_populates="veriff_verifications")
    person: Mapped["VeriffPerson"] = relationship(back_populates="verification")
    document: Mapped["VeriffDocument"] = relationship(back_populates="verification")
    

class VeriffPerson(Base):
    __tablename__ = "veriff_person"

    id: Mapped[int] = mapped_column(primary_key=True)
    verification_id: Mapped[UUID] = mapped_column(ForeignKey("veriff_verification.id"))

    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    date_of_birth: Mapped[date] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(nullable=True)
    nationality: Mapped[str] = mapped_column(nullable=True)
    id_number: Mapped[str] = mapped_column(nullable=True)

    verification: Mapped[VeriffVerification] = relationship(back_populates="person")


class VeriffDocument(Base):
    __tablename__ = "veriff_document"

    id: Mapped[int] = mapped_column(primary_key=True)
    verification_id: Mapped[UUID] = mapped_column(ForeignKey("veriff_verification.id"))

    number: Mapped[str] = mapped_column(nullable=True)
    valid_from: Mapped[date] = mapped_column(nullable=True)
    valid_until: Mapped[date] = mapped_column(nullable=True)
    type: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)

    verification: Mapped["VeriffVerification"] = relationship(back_populates="document")
