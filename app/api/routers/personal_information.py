from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import services
from app.api import schemas
from app.auth import get_user
from app.database import get_session, models

router = APIRouter(prefix="/personal_information")


@router.post("/", response_model=schemas.PersonalInformation)
def save_personal_information(
    data: schemas.PersonalInformationCreate,
    user: models.User = Depends(get_user),
    session: Session = Depends(get_session),
):
    return services.users.update_personal_information(session, user, data)


@router.get("/", response_model=schemas.PersonalInformation)
def get_personal_information(user: models.User = Depends(get_user)):
    return services.users.get_personal_information(user)
