from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_session, models
from app.services import jwt, users

token_auth_scheme = HTTPBearer()


def get_user_id(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)) -> UUID:
    """Extracts the user id from the decoded jwt token."""

    try:
        claims = jwt.get_claims(token.credentials)
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid credentials") from e

    return UUID(claims.get("sub"))


def get_user(
    user_id: UUID = Depends(get_user_id), session: Session = Depends(get_session)
) -> models.User:
    """Gets the user from the database."""

    user = users.get_user_by_id(session, user_id)

    return user
