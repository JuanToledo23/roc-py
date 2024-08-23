from loguru import logger
from sqlalchemy.orm import Session

from app.database import models
from app.exceptions import ValidationError
from app.services import users, verification, jwt


def login(session: Session, phone: str, channel: str) -> None:
    """Send a verification code to a user's phone number."""

    user = users.get_user_by_phone(session, phone)

    verification.send_code(user, channel)


def sign_up(session: Session, phone: str, email: str) -> models.User:
    """Create a new user and send a verification code to their phone number."""

    user = users.create_user(session, phone, email)

    verification.send_code(user)

    return user


def verify(session: Session, phone: str, code: str) -> str:
    """Verify a user's phone number and return a JWT."""

    user = users.get_user_by_phone(session, phone)

    if not verification.verify_code(user, code):
        raise ValidationError("Invalid code")

    logger.info(f"User logged in: {user.id}")

    return jwt.get_token(user)
