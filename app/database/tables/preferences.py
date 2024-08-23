from sqlalchemy import Column, ForeignKey, Table

from app.database import Base

user_preference = Table(
    "profile_preference",
    Base.metadata,
    Column("profile_id", ForeignKey("profile.id")),
    Column("preference_id", ForeignKey("preference.id")),
)
