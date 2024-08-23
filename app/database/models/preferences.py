from datetime import datetime
from enum import Enum

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PreferenceType(Enum):
    personality = "personality"
    roomie = "roomie"
    place = "place"


class Preference(Base):
    __tablename__ = "preference"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[PreferenceType]
    is_active: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())
