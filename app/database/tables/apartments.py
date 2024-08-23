from sqlalchemy import Column, ForeignKey, Table

from app.database.base import Base

apartment_plan = Table(
    "apartment_plan",
    Base.metadata,
    Column("apartment_id", ForeignKey("apartment.id")),
    Column("plan_id", ForeignKey("plan.id")),
)
