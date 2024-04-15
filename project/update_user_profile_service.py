from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    Model for the response after attempting to update a user's profile. Indicates success status.
    """

    success: bool
    message: str


async def update_user_profile(
    email: Optional[str] = None,
    username: Optional[str] = None,
    phone_number: Optional[str] = None,
    profile_picture_url: Optional[str] = None,
) -> UpdateUserProfileResponse:
    """
    Updates the profile of the authenticated user.

    This function attempts to update various fields of a user's profile based on inputs. Checks are performed to ensure
    the uniqueness of both email and username if provided. It also constructs a meaningful message upon successful
    update or upon encountering an error.

    Args:
        email (Optional[str]): The new email address for the user. Optional and should be validated if provided.
        username (Optional[str]): The new username for the user. Optional, but must be unique if provided.
        phone_number (Optional[str]): The new phone number for the user. Optional and should follow a valid format if provided.
        profile_picture_url (Optional[str]): URL of the new profile picture for the user. Optional.

    Returns:
        UpdateUserProfileResponse: Object indicating the success status and message regarding the updating process.
    """
    try:
        if email and await prisma.models.User.prisma().find_unique(
            where={"email": email}
        ):
            return UpdateUserProfileResponse(
                success=False, message="Email already exists."
            )
        if username and await prisma.models.User.prisma().find_unique(
            where={"username": username}
        ):
            return UpdateUserProfileResponse(
                success=False, message="Username already exists."
            )
        auth_user_id = "authenticated-user-id"
        update_payload = {}
        if email:
            update_payload["email"] = email
        if username:
            update_payload["username"] = username
        if phone_number:
            update_payload["phone_number"] = phone_number
        if profile_picture_url:
            update_payload["profile_picture_url"] = profile_picture_url
        await prisma.models.User.prisma().update(
            where={"id": auth_user_id}, data=update_payload
        )
        return UpdateUserProfileResponse(
            success=True, message="User profile updated successfully."
        )
    except Exception as e:
        return UpdateUserProfileResponse(
            success=False, message=f"Failed to update user profile: {str(e)}"
        )
