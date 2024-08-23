import os

from dotenv import load_dotenv

load_dotenv()

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "")

# JWT settings
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")

# Stripe settings
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")
STRIPE_ENDPOINT_SECRET = os.getenv("STRIPE_ENDPOINT_SECRET", "")

# Assets settings
ASSETS_URL = os.getenv("ASSETS_URL", "https://roc-space.imgix.net")

# Twilio settings
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_VERIFY_SERVICE_SID = os.getenv("TWILIO_VERIFY_SERVICE_SID", "")

# Verification settings
VERIFICATION_TEST_PHONES = os.getenv("VERIFICATION_TEST_PHONES", "").split(",")
VERIFICATION_TEST_CODE = os.getenv("VERIFICATION_TEST_CODE", "123456")

# Veriff settings
VERIFF_API_KEY = os.getenv("VERIFF_API_KEY", "")
VERIFF_BASE_URL = os.getenv("VERIFF_BASE_URL", "")
VERIFF_SHARED_SECRET_KEY = os.getenv("VERIFF_SHARED_SECRET_KEY", "")
