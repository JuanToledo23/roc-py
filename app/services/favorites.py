from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import models, tables


def get_favorite_zones(session: Session, user: models.User):
    """Get all zones and whether or not they are selected by the user."""

    zones = session.execute(
        select(
            models.Zone,
            select(tables.zone_favorite)
            .where(
                tables.zone_favorite.c.profile_id == user.id,
                tables.zone_favorite.c.zone_id == models.Zone.id,
            )
            .exists()
            .label("is_selected"),
        ).where(models.Zone.is_active.is_(True))
    ).all()

    return [
        {
            "id": zone.id,
            "name": zone.name,
            "description": zone.description,
            "assets": zone.assets,
            "is_selected": is_selected,
        }
        for (zone, is_selected) in zones
    ]


def update_favorite_zones(session: Session, user: models.User, zone_ids: list[int]):
    """Update the user's selected zones."""

    zones = session.scalars(
        select(models.Zone).where(models.Zone.id.in_(zone_ids))
    ).all()

    user.zone_favorites.clear()

    for zone in zones:
        user.zone_favorites.append(zone)

    session.commit()

    logger.info(f"Favorite zones updated: {user.id}")
