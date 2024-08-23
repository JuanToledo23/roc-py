from loguru import logger
from twilio.base.exceptions import TwilioRestException

from app import settings
from app.database import models
from app.integrations import twilio

verify = twilio.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_SID)


def send_code(user: models.User, channel: str = "sms"):
    """Send a verification code to a user's phone number."""

    if user.phone in settings.VERIFICATION_TEST_PHONES:
        logger.info(f"Not sending verification phone (test phone) {user.phone}")

        return

    logger.info(f"Sending verification code to {user.phone}")

    result = verify.verifications.create(to=user.phone, channel=channel)

    logger.info(f"Verification result: {result}")


def verify_code(user: models.User, code: str) -> bool:
    """Verify the code sent to a user's phone number."""

    if user.phone in settings.VERIFICATION_TEST_PHONES:
        logger.info(f"Test phone verification: {user.phone}")

        return code == settings.VERIFICATION_TEST_CODE

    try:
        result = verify.verification_checks.create(to=user.phone, code=code)
    except TwilioRestException as e:
        logger.error(f"Error while verifying code: {e}")

        return False

    logger.info(f"Verification result: {result}")

    return result.status == "approved"
