from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api import schemas
from app.auth import get_user_id
from app.database import get_session, models

router = APIRouter(
    prefix="/applications",
    tags=["applications"],
)


@router.get("/")
def get_application(
    user_id: UUID = Depends(get_user_id),
    session: Session = Depends(get_session),
):
    applications = session.scalars(
        select(models.Application).order_by(models.Application.created_at.desc())
    )

    return [
        schemas.Application.model_validate(application) for application in applications
    ]


@router.post("/")
def create_application(
    data: schemas.ApplicationCreate,
    user_id: UUID = Depends(get_user_id),
    session: Session = Depends(get_session),
):
    room = session.get(models.Room, data.room_id)

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if not room.is_active:
        raise HTTPException(status_code=400, detail="Room is not active")

    if not room.is_available:
        # TODO: Check if the room is available in the future
        raise HTTPException(status_code=400, detail="Room is not available")

    plan = next(filter(lambda plan: plan.id == data.plan_id, room.plans), None)

    if not plan:
        raise HTTPException(
            status_code=400, detail="The plan is not available for the selected room"
        )

    application = models.Application(
        room=room,
        plan=plan,
        start_date=data.start_date,
        profile_id=user_id,
    )

    session.add(application)
    session.commit()
    session.refresh(application)

    return schemas.Application.model_validate(application)


@router.patch("/{application_id}")
def update_application(
    application_id: int,
    data: schemas.ApplicationUpdate,
    user_id: UUID = Depends(get_user_id),
    session: Session = Depends(get_session),
):
    application = session.get(models.Application, application_id)

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if application.status != models.ApplicationStatus.pending:
        raise HTTPException(
            status_code=400, detail="Application can't be updated at this time"
        )

    if application.profile_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if data.plan_id:
        plan = next(
            filter(lambda plan: plan.id == data.plan_id, application.room.plans), None
        )

        if not plan:
            raise HTTPException(
                status_code=400,
                detail="The plan is not available for the selected room",
            )

        application.plan = plan

    if data.start_date:
        application.start_date = data.start_date

    session.commit()

    return schemas.Application.model_validate(application)
