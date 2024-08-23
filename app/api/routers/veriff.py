from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app import services
from app.api import schemas
from app.auth import get_user
from app.database import models, get_session
from app.utils import get_raw_body

router = APIRouter(
    prefix="/veriff",
)


@router.get("/session", response_model=schemas.VeriffSession, response_model_by_alias=False)
def get_session_url(
        user: models.User = Depends(get_user),
        session: Session = Depends(get_session),
    ):
    return services.veriff.get_session_url(user, session)


@router.post("/webhook_events")
def webhook_events(
        body: bytes = Depends(get_raw_body),
        x_hmac_signature: Annotated[str, Header()] = '',
    ):  
    return services.veriff.handle_event_webhook_events(body, x_hmac_signature)


@router.post("/webhook_full_auto")
def webhook_full_auto(
        body: bytes = Depends(get_raw_body),
        session: Session = Depends(get_session),
        x_hmac_signature: Annotated[str, Header()] = '',
    ):
    return services.veriff.handle_event_webhook_full_auto(body, session, x_hmac_signature)
