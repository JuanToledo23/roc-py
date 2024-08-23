import json
from typing import Any, Literal

import requests
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import settings
from app.utils import validate_hmac_signature
from app.database import models
from app.exceptions import ValidationError


def lazy_get_value(key: str, data: dict[str, Any], /) -> Any:
    """Tries to retrieve key value if key exists else returns None"""
    obj = data.get(key, None)
    if not isinstance(obj, dict):
        return None
    return data[key]['value']


def api_request(
        method: Literal['GET', 'PUT', 'POST', 'DELETE'],
        *path: str,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
    """Sends a veriff api request and returns response."""
    api_url = '/'.join([settings.VERIFF_BASE_URL, *path])
    headers = {
        'X-AUTH-CLIENT': settings.VERIFF_API_KEY,
    }
    response = requests.request(method, api_url, json=body, headers=headers)
    if not response.ok:
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f'request failed: {method} {api_url}')
            logger.exception(e)
            raise ValidationError('veriff api request failed') 
    
    return response.json()


def get_session_url(
        user: models.User,
        session: Session,
        /,
    ) -> models.VeriffSession:
    """Returns veriff session url."""
    veriff_session = session.scalar(
        select(models.VeriffSession)
            .where(
                models.VeriffSession.is_active,
                models.VeriffSession.profile_id == user.id, 
            )
    )

    if veriff_session:
        return veriff_session

    body = {
        'verification': {
            'vendorData': str(user.id),
        },
    }
    response = api_request('POST', 'v1', 'sessions', body=body)

    veriff_session = models.VeriffSession(
        id=response['verification']['id'],
        profile_id=user.id,
        url=response['verification']['url'],
        status=response['verification']['status'],
    )
    session.add(veriff_session)
    session.commit()
    session.refresh(veriff_session)

    logger.info(f'Created Veriff Session: {veriff_session.id}')

    return veriff_session


def create_verification(
        event: dict[str, Any], 
        session: Session,
        /,
    ):
    """Creates a veriff verification"""

    user_id = event['vendorData']
    verification_id = event['sessionId']
    veriff_session = session.get(models.VeriffSession, verification_id)
    if not veriff_session:
        logger.error('Veriff session not found')
        raise ValidationError('Session not found')
    
    veriff_verification = session.get(models.VeriffVerification, verification_id)
    if veriff_verification:
        logger.error(f'Veriff verification already exists: {verification_id}')
        return

    verification_data = event['data']['verification']
    decision = verification_data['decision']

    veriff_session.status = decision

    verification = models.VeriffVerification(
        id=verification_id,
        profile_id=user_id,
        decision=decision,
        response=verification_data,
    )
    
    person_data = verification_data['person']
    person = models.VeriffPerson(
        verification_id=verification.id,
        first_name=lazy_get_value('firstName', person_data),
        last_name=lazy_get_value('lastName', person_data),
        date_of_birth=lazy_get_value('dateOfBirth', person_data),
        gender=lazy_get_value('gender', person_data),
        nationality=lazy_get_value('nationality', person_data),
        id_number=lazy_get_value('idNumber', person_data),
    )

    document_data = verification_data['document']
    document = models.VeriffDocument(
        verification_id=verification.id,
        number=lazy_get_value('number', document_data),
        valid_from=lazy_get_value('validFrom', document_data),
        valid_until=lazy_get_value('validUntil', document_data),
        type=lazy_get_value('type', document_data),
        country=lazy_get_value('country', document_data),
    )

    session.add(verification)
    session.add(person)
    session.add(document)
    session.add(veriff_session)
    session.commit()

    logger.info(f'Completed Veriff Verification: {verification_id} - {decision}')


def update_verification(
        event: dict[str, Any], 
        session: Session,
        /,
    ):
    """Updates session status and verification decision."""
    user_id = event['vendorData']
    verification_id = event['sessionId']
    veriff_session = session.get(models.VeriffSession, verification_id)
    veriff_verification = session.get(models.VeriffVerification, verification_id)
    if not veriff_session:
        logger.error('Veriff session not found')
        raise ValidationError('Session not found')
    if not veriff_verification:
        logger.error('Veriff verification not found')
        raise ValidationError('Verification not found')

    decision = event['data']['verification']['decision']
    veriff_session.status = decision
    veriff_verification.decision = decision

    session.add(veriff_session)
    session.add(veriff_verification)
    session.commit()

    logger.info(f'Updated Veriff Verification: {verification_id} - {decision}')


def handle_event_webhook_events(
        body: bytes,
        signature: str,
        /,
    ):
    """Handles events wehbook events."""

    secret_key = settings.VERIFF_SHARED_SECRET_KEY.encode()
    if not validate_hmac_signature(body, signature, secret_key):
        logger.error('Signature validation failed')
        raise ValidationError('Signature validation failed')

    event = json.loads(body)
    logger.info('Received Veriff Event')


def handle_event_webhook_full_auto(
        body: bytes,
        session: Session,
        signature: str,
        /,
    ):
    """Handles full auto webhook events."""

    secret_key = settings.VERIFF_SHARED_SECRET_KEY.encode()
    if not validate_hmac_signature(body, signature, secret_key):
        logger.error('Signature validation failed')
        raise ValidationError('Signature validation failed')

    event = json.loads(body)
    if event['status'] != 'success':
        logger.error(f'Unknown event status: {event["status"]}')
        raise ValidationError('Unknown event status')

    match event['data']['verification']['decision']:
        case 'approved':
            create_verification(event, session)
        case _:
            update_verification(event, session)
