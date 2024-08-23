from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import services
from app.api import schemas
from app.auth import get_user
from app.database import get_session, models

router = APIRouter(prefix="/preferences")


@router.get("", response_model=list[schemas.Preference])
def get_preferences(
    type: models.PreferenceType,
    user: models.User = Depends(get_user),
    session: Session = Depends(get_session),
):
    return services.preferences.get_preferences(session, user, type)


@router.post("/", status_code=204)
def update_preferences(
    body: schemas.PreferenceUpdate,
    user: models.User = Depends(get_user),
    session: Session = Depends(get_session),
):
    services.preferences.update_preferences(session, user, body)
