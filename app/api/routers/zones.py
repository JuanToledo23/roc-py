from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api import schemas
from app.database import get_session, models

router = APIRouter(
    prefix="/zones",
    tags=["zones"],
)


@router.get("", response_model=list[schemas.Zone])
def get_zones(session: Session = Depends(get_session)):
    """Get all active zones."""

    zones = session.scalars(
        select(models.Zone).where(models.Zone.is_active.is_(True)),
    ).all()

    return zones


@router.get("/{zone_id}", response_model=schemas.Zone)
def get_zone(zone_id: int, session: Session = Depends(get_session)):
    """Get a zone by ID."""

    zone = session.get(models.Zone, zone_id)

    if not zone or not zone.is_active:
        raise HTTPException(status_code=404, detail="Zone not found")

    return zone
