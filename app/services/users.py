from uuid import UUID

from loguru import logger
from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from app.api import schemas
from app.database import models
from app.exceptions import NotFoundError, ValidationError


def get_user_by_phone(session: Session, phone: str) -> models.User:
    """Get a user by phone number."""

    user = session.scalar(select(models.User).where(models.User.phone == phone))

    if not user:
        logger.error(f"User not found: {phone}")

        raise NotFoundError("User not found")

    return user


def get_user_by_id(session: Session, id: UUID) -> models.User:
    """Get a user by id."""

    user = session.get(models.User, id)

    if not user:
        logger.error(f"User not found: {id}")

        raise NotFoundError("User not found")

    return user


def exists_by_phone(session: Session, phone: str) -> bool:
    """Check if a user exists by phone number."""

    return session.scalar(
        exists().where(models.User.phone == phone).select()
    )


def exists_by_email(session: Session, email: str) -> bool:
    """Check if a user exists by email."""

    return session.scalar(
        exists().where(models.User.email == email).select()
    )


def create_user(session: Session, phone: str, email: str) -> models.User:
    """Create a new user."""

    if exists_by_email(session, email):
        logger.error(f"User already exists: {email}")

        raise ValidationError("Email already in use")

    if exists_by_phone(session, phone):
        logger.error(f"User already exists: {phone}")

        raise ValidationError("Phone already in use")

    user = models.User(email=email, phone=phone)

    session.add(user)
    session.commit()

    logger.info(f"User created: {user.id}")

    return user


def update_user(session: Session, user: models.User, data: schemas.UserUpdate) -> models.User:
    """Update a user."""

    user.name = data.name
    user.date_of_birth = data.date_of_birth
    user.is_completed = True

    session.commit()

    logger.info(f"User updated: {user.id}")

    return user


def get_personal_information(user: models.User) -> models.PersonalInformation:
    """Get a user's personal information."""

    if not user.personal_information:
        logger.error(f"Personal information not found: {user.id}")

        raise NotFoundError("Personal information not found")

    return user.personal_information


def update_personal_information(session: Session, user: models.User,
                                data: schemas.PersonalInformationCreate) -> models.PersonalInformation:
    if user.personal_information:
        logger.error(f"Personal Information already exists: {user.id}")

        raise ValidationError(
            "Personal information already exists"
        )

    information = models.PersonalInformation(
        profile_id=user.id,
        first_name=data.first_name,
        last_name=data.last_name,
        date_of_birth=data.date_of_birth,
        gender=data.gender,
    )

    session.add(information)
    session.commit()

    logger.info(f"Personal Information updated: {user.id}")

    session.refresh(information)

    return information
