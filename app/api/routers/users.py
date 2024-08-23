from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import services
from app.api import schemas
from app.auth import get_user
from app.database import models, get_session

router = APIRouter(
    prefix="/users",
)


@router.get("/me", response_model=schemas.User)
def get_profile(user: models.User = Depends(get_user)):
    return user


@router.put("/me", response_model=schemas.User)
def update_profile(data: schemas.UserUpdate, user: models.User = Depends(get_user),
                   session: Session = Depends(get_session)):
    return services.users.update_user(session, user, data)
