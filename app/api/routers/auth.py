from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import services
from app.api import schemas
from app.database import get_session

router = APIRouter(prefix="/auth")


@router.post("/login", status_code=204)
def login(body: schemas.Login, session: Session = Depends(get_session)):
    services.auth.login(session, body.phone, body.channel)


@router.post("/signup", status_code=204)
def signup(body: schemas.SignUp, session: Session = Depends(get_session)):
    services.auth.sign_up(session, body.phone, body.email)


@router.post("/verify")
def verify(body: schemas.Verify, session: Session = Depends(get_session)):
    token = services.auth.verify(session, body.phone, body.code)

    return {"token": token}
