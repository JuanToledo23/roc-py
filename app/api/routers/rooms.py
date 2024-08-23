from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import services
from app.api import schemas
from app.database import get_session

router = APIRouter(
    prefix="/rooms",
)


@router.get("", response_model=list[schemas.Room])
def get_rooms(
    session: Session = Depends(get_session),
    building_id: int | None = None,
):
    return services.rooms.get_rooms(session, building_id=building_id)


@router.get("/featured", response_model=list[schemas.Room])
def get_featured_rooms(session: Session = Depends(get_session)):
    return services.rooms.get_rooms(session, limit=10, order=True)


@router.get("/{room_id}", response_model=schemas.Room)
def get_room(
        room_id: int,
        session: Session = Depends(get_session),
    ):
    return services.rooms.get_room_by_id(room_id, session)


@router.get("/{room_id}/plans", response_model=list[schemas.RoomPlan])
def get_room_plans(
        room_id: int,
        session: Session = Depends(get_session),
    ):
    return services.rooms.get_room_plans(room_id, session)


@router.get("/{room_id}/calendar", response_model=schemas.RoomCalendar)
def get_room_calendar(
        room_id: int,
        session: Session = Depends(get_session),
    ):
    return services.rooms.get_room_calendar(room_id, session)
