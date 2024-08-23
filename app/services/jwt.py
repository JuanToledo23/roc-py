from datetime import datetime, timedelta

from jose import jwt

from app import settings
from app.database import models


def get_token(user: models.User) -> str:
    """Generate a JWT token for a user."""

    now = datetime.now()
    issued_at = int(now.timestamp())
    expiration = int((now + timedelta(days=365)).timestamp())

    claims = {"sub": str(user.id), "iat": issued_at, "exp": expiration,
              "email": user.email,
              "phone": user.phone}

    return jwt.encode(
        claims,
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM,
    )


def get_claims(token: str) -> dict:
    """Decode a JWT token and return the claims."""

    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
