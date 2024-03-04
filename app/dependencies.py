import hashlib
import hmac
import logging
from typing import Annotated, Union

from fastapi import (
    Header, HTTPException, Request
)

from .config import Settings

logger = logging.getLogger(__name__)
settings = Settings()


def verify_signature(secret: Union[bytes, str], signature: str, payload: bytes) -> bool:
    """
    Verifies a signature by comparing a hash of the `payload` to `signature`.
    Notes:
         - netbox uses a 512 SHA hash other webhooks may not use the same
         - all encoding/decoding is `UTF-8`
    Args:
        secret: (bytes) the secret used to generate the HMAC
        signature: (str) a hex digest from the client
        payload: (bytes) the encoded payload

    Returns:
        (bool) True on match
    """
    print(f"secret: {secret}, type: {type(secret)}, enc: {secret.encode('utf-8')}")
    print(f"payload: {payload}")
    hashed = hmac.new(
        secret if isinstance(secret, bytes) else secret.encode('utf-8'),
        payload,
        hashlib.sha512).hexdigest()
    print(f"sec :{secret}\ncalc:{hashed}\nsig :{signature}")
    logger.info(f"calc:{hashed}\nsig :{signature}")
    return hashed == signature


async def get_x_hook_signature_header(x_hook_signature: Annotated[str, Header()], payload: Request):
    """
    Extract header `X-Hook-Signature` then verify the signature.
    Args:
        x_hook_signature: (str) a hex digest from the client
        payload: (bytes) the encoded payload

    Notes: see verify_signature(...) for more info. This method only supports nautobot but could be extended
    to support other webhooks that use a 512 X-Hook-Signature
    """
    print(f"get_token_header: {x_hook_signature}")
    data = await payload.body()
    # print(f"data: {type(data)}, {data}")
    if not verify_signature(settings.netbox_secret, x_hook_signature, data):
        raise HTTPException(status_code=400, detail="X-Hook-Signature header invalid")
