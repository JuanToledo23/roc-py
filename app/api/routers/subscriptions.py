from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import schemas
from app.auth import get_user_id
from app.database import get_session, models

router = APIRouter(
    prefix="/subscriptions",
)


@router.get("/")
def get_subscriptions(
    user_id: UUID = Depends(get_user_id), session: Session = Depends(get_session)
):
    profile = session.get(models.User, user_id)

    return [
        schemas.Subscription.model_validate(subscription)
        for subscription in profile.subscriptions
    ]


@router.post("/")
def create_subscription(
    data: schemas.SubscriptionCreate,
    user_id: UUID = Depends(get_user_id),
    session: Session = Depends(get_session),
):
    profile = session.get(models.User, user_id)
    room = session.get(models.Room, data.room_id)
    plan = session.get(models.Plan, data.plan_id)

    subscription = models.Subscription(
        profile=profile,
        room=room,
        plan=plan,
        starts_at=data.starts_at,
        ends_at=data.starts_at + timedelta(days=30 * plan.duration),
        amount=room.monthly_price + (room.monthly_price * plan.fee),
    )

    session.add(subscription)

    session.commit()
    session.refresh(subscription)

    return schemas.Subscription.model_validate(subscription)
