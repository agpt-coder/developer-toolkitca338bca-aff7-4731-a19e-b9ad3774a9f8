from datetime import datetime, timedelta

import jwt
import prisma
import prisma.models
from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    """
    Model for the response after refreshing the JWT token.
    """

    access_token: str
    token_type: str
    expires_in: int


SECRET_KEY = "your_very_secret_key"

ALGORITHM = "HS256"


async def refresh_token(refresh_token: str) -> RefreshTokenResponse:
    """
    Refreshes the authentication token if it's expired but the refresh token is still valid.

    Args:
        refresh_token (str): The refresh token provided by the user during their last authentication process.

    Returns:
        RefreshTokenResponse: A model including a new access token, its type, and expiry duration in seconds.

    Raises:
        ValueError: If the provided refresh token is invalid or expired, or if the associated user is not found.
    """
    token_record = await prisma.models.APIToken.prisma().find_first(
        where={"token": refresh_token, "expiresAt": {"gt": datetime.now()}},
        include={"prisma.models.User": True},
    )
    if token_record is None or token_record.User is None:
        raise ValueError("Invalid or expired refresh token.")
    new_access_token_payload = {
        "user_id": token_record.User.id,
        "role": token_record.User.role,
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    new_access_token = jwt.encode(
        new_access_token_payload, SECRET_KEY, algorithm=ALGORITHM
    )
    return RefreshTokenResponse(
        access_token=new_access_token, token_type="bearer", expires_in=1800
    )
