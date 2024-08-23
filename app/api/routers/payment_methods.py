from uuid import UUID

import stripe
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import schemas
from app.auth import get_user_id
from app.database import get_session, models

router = APIRouter(prefix="/payment_methods")


@router.get("/")
def get_payment_methods(
    user_id: UUID = Depends(get_user_id), session: Session = Depends(get_session)
):
    profile = session.get(models.User, user_id)

    return [
        schemas.PaymentMethod.model_validate(payment_method)
        for payment_method in filter(
            lambda payment_method: payment_method.is_active, profile.payment_methods
        )
    ]


@router.post("/")
def create_payment_method(
    data: schemas.PaymentMethodCreate,
    user_id: UUID = Depends(get_user_id),
    session: Session = Depends(get_session),
):
    profile = session.get(models.User, user_id)

    stripe_payment_method = stripe.PaymentMethod.create(type="card", card={"token": ""})

    if data.is_default:
        for p in profile.payment_methods:
            p.is_default = False

    payment_method = models.PaymentMethod(
        profile=profile,
        is_default=data.is_default,
    )

    session.add(payment_method)

    session.commit()
    session.refresh(payment_method)

    return schemas.PaymentMethod.model_validate(payment_method)


@router.delete("/{payment_method_id}", status_code=204)
def delete_payment_method(
    payment_method_id: int,
    user_id: UUID = Depends(get_user_id),
    session: Session = Depends(get_session),
):
    profile = session.get(models.User, user_id)
    payment_method = session.get(models.PaymentMethod, payment_method_id)

    if not payment_method:
        raise HTTPException(404, detail="Payment method not found")

    if payment_method.profile_id != profile.id:
        raise HTTPException(403, detail="Forbidden")

    payment_method.is_active = False

    session.commit()
