from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api import schemas
from app.database import models, tables


def get_preferences(session: Session, user: models.User, type: models.PreferenceType):
    """Get preferences for a user of a given type."""

    preferences = session.execute(
        select(
            models.Preference,
            select(tables.user_preference)
            .where(
                tables.user_preference.c.profile_id == user.id,
                tables.user_preference.c.preference_id == models.Preference.id,
            )
            .exists()
            .label("is_selected"),
        ).where(
            models.Preference.is_active.is_(True),
            models.Preference.type == type,
        ),
    ).all()

    return [
        {
            "id": preference.id,
            "name": preference.name,
            "is_selected": is_selected,
        }
        for (preference, is_selected) in preferences
    ]


def update_preferences(session: Session, user: models.User, data: schemas.PreferenceUpdate):
    """Update preferences for a user of a given type."""

    old_preferences = session.scalars(
        select(models.Preference)
        .join(
            tables.user_preference,
            tables.user_preference.c.preference_id == models.Preference.id,
        )
        .where(
            models.Preference.type == data.type,
            tables.user_preference.c.profile_id == user.id,
            models.Preference.id.notin_(data.ids),
        )
    ).all()

    for preference in old_preferences:
        user.preferences.remove(preference)

    new_preferences = session.scalars(
        select(models.Preference).where(models.Preference.id.in_(data.ids))
    ).all()

    for preference in new_preferences:
        user.preferences.append(preference)

    session.commit()

    logger.info(f"Preferences updated: {data.type.value},  {user.id}")
