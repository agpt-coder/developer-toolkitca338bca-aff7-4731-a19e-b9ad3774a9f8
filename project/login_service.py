from datetime import datetime, timedelta

import jwt
import prisma
import prisma.models
from passlib.hash import bcrypt
from pydantic import BaseModel


class UserInfo(BaseModel):
    """
    Defines basic user information returned upon successful authentication.
    """

    email: str
    role: str


class LoginResponse(BaseModel):
    """
    Represents the output after a successful login, including the JWT and possibly some basic user information.
    """

    jwt_token: str
    user_info: UserInfo


SECRET_KEY = "YOUR_SECRET_KEY"

JWT_ALGORITHM = "HS256"


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the provided plain password matches the hashed password by checking if
    the hash of the plain password is equal to the stored hash.

    Args:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: Whether the password is correct.
    """
    return bcrypt.verify(plain_password, hashed_password)


async def login(email: str, password: str) -> LoginResponse:
    """
    Handles user login and returns a JWT along with basic user information
    if authentication is successful.

    Args:
        email (str): The email address used by the user to login.
        password (str): The password provided by the user for logging in.

    Returns:
        LoginResponse: Contains the JWT and user information if authentication succeeds.

    Raises:
        ValueError: If the email does not exist or the password is incorrect.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user is None or not await verify_password(password, user.hash):
        raise ValueError("Incorrect email or password.")
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(days=1),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return LoginResponse(
        jwt_token=token, user_info=UserInfo(email=user.email, role=user.role)
    )
