import stripe
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy import update, select

from app.database import models
from app.exceptions import ValidationError
from app import settings


def get_stripe_cards(
        user: models.User,
        session: Session,
        /,
    ):
    return session.scalars(
        select(models.StripeCard)
            .where(
                models.StripeCard.is_active,
                models.StripeCard.profile_id == user.id, 
            )
    ).all()


def create_stripe_card(
        session: Session,
        setup_intent: stripe.SetupIntent,
        /,
    ):
    """Creates a new `StripeCard`."""

    profile_id = setup_intent.metadata['user_id']

    session.execute(
        update(models.StripeCard)
            .where(models.StripeCard.profile_id == profile_id)
            .values(is_active=False)
    )

    stripe_card = models.StripeCard(
        id=setup_intent.payment_method.id,
        profile_id=profile_id,
        brand=setup_intent.payment_method.card.brand,
        funding=setup_intent.payment_method.card.funding,
        last4=setup_intent.payment_method.card.last4,
        exp_month=setup_intent.payment_method.card.exp_month,
        exp_year=setup_intent.payment_method.card.exp_year,
    )

    session.add(stripe_card)
    session.commit()

    logger.info('Created stripe card', stripe_card)


def handle_event(
        raw_body: bytes,
        session: Session,
        signature: str,
        /,
    ):
    """Handles incoming events from Stripe."""
    try:

        event = stripe.Webhook.construct_event(raw_body, signature, settings.STRIPE_ENDPOINT_SECRET)
    except ValueError as e:
        logger.error('Error parsing payload', e)
        raise ValidationError('Error parsing payload')
    except stripe.error.SignatureVerificationError as e:
        logger.error('Error verifying webhook signature', e)
        raise ValidationError('Error verifying webhook signature')

    match event.type:
        case 'setup_intent.succeeded':
            setup_intent = stripe.SetupIntent.retrieve(
                id=event.data.object.id,
                api_key=stripe.api_key,
                expand=['payment_method'],
            )
            create_stripe_card(session, setup_intent)
        case _:
            logger.error(f"Unhandled event type: {event.type}")
