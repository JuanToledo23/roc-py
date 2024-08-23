from datetime import date
from calendar import Calendar

from sqlalchemy.orm import Session
from sqlalchemy import select
from loguru import logger

from app.database import models
from app.exceptions import NotFoundError, ValidationError


def calculate_room_price(
        room: models.Room, 
        plan: models.Plan,
        /,
    ) -> float:
    """Calculates room price based on plan attributes."""
    with_fee = room.monthly_price + (plan.fee * room.monthly_price)
    discount = with_fee * plan.discount
    return with_fee - discount


def get_rooms(
        session: Session,
        building_id: int | None = None,
        limit: int | None = None,
        order: bool = False,
    ):
    """Returns active rooms."""
    
    query = select(models.Room).where(models.Room.is_active)
    
    if building_id:
        query = query.where(models.Room.building_id == building_id)

    if limit:
        query = query.limit(limit)

    if order:
        query = query.order_by(models.Room.created_at)

    return session.scalars(query)


def get_room_by_id(
        room_id: int, 
        session: Session,
        /,
    ) -> models.Room:
    """Returns room by id."""
    room = session.get(models.Room, room_id)
    if not room:
        logger.error("Room not found")
        raise NotFoundError("Room not found")
    return room


def get_active_room_by_id(
        room_id: int,
        session: Session,
        /,
    ) -> models.Room:
    """Returns room by id if is active and available."""
    room = get_room_by_id(room_id, session)
    if not room.is_active:
        logger.error("Room is not active")
        raise ValidationError("Room is not active")
    if not room.is_available:
        logger.error("Room is not available")
        raise ValidationError("Room is not available")
    return room


def get_room_calendar(
        room_id: int,
        session: Session,
        /,
    ) -> dict[str, date | list[date]]:
    """Returns room calendar."""
    room = get_active_room_by_id(room_id, session)
    
    calendar = Calendar(firstweekday=6)
    available_at = room.available_at.date()

    year = available_at.year if available_at.month < 12 else available_at.year + 1
    month = available_at.month + 1 if available_at.month < 12 else 1

    dates: list[date] = []
    for week in calendar.monthdatescalendar(year, month)[:2]:
        for day in week:
            if day.month == month:
                dates.append(day)

    return {
        'since': dates[0],
        'available_at': dates,
    }


def get_room_plans(
        room_id: int,
        session: Session,
        /,
    ) -> list[dict[str, int | float | str]]:
    """Returns room plans sorted by duration."""
    room = get_active_room_by_id(room_id, session)
    plans = [
        {
            "id": plan.id,
            "code": plan.code,
            "duration": plan.duration,
            "monthly_price": calculate_room_price(room, plan),
            "discount": plan.discount,
        }
        for plan in room.plans
    ]
    return sorted(plans, key=lambda p: p["duration"])  
