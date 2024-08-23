import hmac
import hashlib
from fastapi import Request


async def get_raw_body(request: Request) -> bytes:
    """Returns requests raw body."""
    return await request.body()


def get_hmac_signature(body: bytes, secret_key: bytes, /) -> str:
    """Returns hmac signature from body."""
    signature = hmac.new(
        key=secret_key, 
        msg=body, 
        digestmod=hashlib.sha256,
    )
    return signature.hexdigest()


def validate_hmac_signature(body: bytes, signature: str, secret_key: bytes, /) -> bool:
    """Compares digests."""
    return hmac.compare_digest(signature, get_hmac_signature(body, secret_key))
