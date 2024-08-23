from typing import Annotated

import stripe
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.auth import get_user
from app.utils import get_raw_body
from app.database import get_session, models
from app.api import schemas
from app import services

router = APIRouter(prefix="/stripe")


@router.get("/setup-intent")
def get_setup_intent(
    user: models.User = Depends(get_user), session: Session = Depends(get_session)
):
    customer = None

    if len(user.stripe_customers) > 0:
        customer = stripe.Customer.retrieve(user.stripe_customers[0].id)
    else:
        customer = stripe.Customer.create(
            email=user.email,
            phone=user.phone,
            name=user.name,
            metadata={"user_id": user.id},
        )

        user.stripe_customers.append(models.StripeCustomer(id=customer.id))

        session.commit()

    intent = stripe.SetupIntent.create(customer=customer.id, metadata={"user_id": user.id},)

    return {"client_secret": intent.client_secret}


@router.get("/cards", response_model=list[schemas.StripeCard])
def get_payment_methods(
        user: models.User = Depends(get_user),
        session: Session = Depends(get_session),
    ):
    return services.stripe.get_stripe_cards(user, session)


@router.post('/webhook')
def webhook(
        raw_body: bytes = Depends(get_raw_body),
        session: Session = Depends(get_session),
        stripe_signature: Annotated[str, Header()] = '',
    ):
    services.stripe.handle_event(raw_body, session, stripe_signature)
