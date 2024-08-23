from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import services
from app.api import schemas
from app.auth import get_user
from app.database import get_session, models

router = APIRouter(prefix="/favorites")


@router.get("/zones", response_model=list[schemas.ZoneFavorite])
def get_zone_favorites(
    user: models.User = Depends(get_user), session: Session = Depends(get_session)
):
    return services.favorites.get_favorite_zones(session, user)


@router.post("/zones", status_code=204)
def create_zone_favorite(
    zone_ids: list[int],
    user: models.User = Depends(get_user),
    session: Session = Depends(get_session),
):
    services.favorites.update_favorite_zones(session, user, zone_ids)


@router.get("/buildings", response_model=list[schemas.Building])
def get_building_favorites(user: models.User = Depends(get_user)):
    return user.building_favorites


@router.post("/buildings", status_code=204)
def create_building_favorite(
    favorite: schemas.BuildingFavorite,
    user: models.User = Depends(get_user),
    session: Session = Depends(get_session),
):
    building = session.get(models.Building, favorite.building_id)

    if not building:
        raise HTTPException(status_code=404, detail="Building not found")

    user.building_favorites.append(building)

    session.commit()


@router.delete("/buildings/{building_id}", status_code=204)
def delete_building_favorite(
    building_id: int,
    user: models.User = Depends(get_user),
    session: Session = Depends(get_session),
):
    building = session.get(models.Building, building_id)

    if not building:
        raise HTTPException(status_code=404, detail="Building not found")

    user.building_favorites.remove(building)

    session.commit()


@router.get("/rooms", response_model=list[schemas.Room])
def get_room_favorites(user: models.User = Depends(get_user)):
    return user.room_favorites


@router.post("/rooms", status_code=204)
def create_room_favorite(
    favorite: schemas.RoomFavorite,
    user: models.User = Depends(get_user),
    session: Session = Depends(get_session),
):
    room = session.get(models.Room, favorite.room_id)

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    user.room_favorites.append(room)

    session.commit()


@router.delete("/rooms/{room_id}", status_code=204)
def delete_room_favorite(
    room_id: int,
    user: models.User = Depends(get_user),
    session: Session = Depends(get_session),
):
    room = session.get(models.Room, room_id)

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    user.room_favorites.remove(room)

    session.commit()
