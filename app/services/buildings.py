from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import models
from app.api import schemas


def get_buildings(
        session: Session,
        near: schemas.Point | None = None,
        limit: int | None = None,
        zone_id: int | None = None,
        order: bool = False,
    ):
    """Returns active buildings."""
    
    query = select(models.Building).where(models.Building.is_active)

    if near:
        query = query.where(models.Building.location.ST_DWithin(near, 10_000))
    
    if zone_id:
        query = query.where(models.Building.zone_id == zone_id)
    
    if limit:
        query = query.limit(limit)

    if order:
        query = query.order_by(models.Building.created_at)

    return session.scalars(query)
