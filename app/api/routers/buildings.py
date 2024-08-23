from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import services
from app.api import schemas
from app.database import get_session, models

router = APIRouter(
    prefix="/buildings",
)


@router.get("", response_model=list[schemas.Building])
def get_buildings(
    near: schemas.Point | None = None,
    zone_id: int | None = None,
    session: Session = Depends(get_session),
):
    return services.buildings.get_buildings(session, near=near, zone_id=zone_id)


@router.get("/featured", response_model=list[schemas.Building])
def get_featured_buildings(session: Session = Depends(get_session)):
    return services.buildings.get_buildings(session, limit=10, order=True)


@router.get("/{building_id}")
def get_building(building_id: int, session: Session = Depends(get_session)):
    building = session.get(models.Building, building_id)

    if not building or not building.is_active:
        raise HTTPException(status_code=404, detail="Building not found")

    return schemas.Building.model_validate(building)
