from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, StrictStr

from corbado_python_sdk.generated.models.user import User
from corbado_python_sdk.generated.models.user_status import UserStatus


class UserEntity(BaseModel):
    """Represents a user entity."""

    user_id: StrictStr = Field(alias="userID")
    full_name: Optional[StrictStr] = Field(default=None, alias="fullName")
    status: UserStatus
    explicit_webauthn_id: Optional[StrictStr] = Field(default=None, alias="explicitWebauthnID")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True, arbitrary_types_allowed=True)

    @classmethod
    def from_user(cls, user: User) -> "UserEntity":
        """Create a UserEntity instance from a User.

        Args:
            user (User): User object

        Returns:
            UserEntity: UserEntity
        """
        return UserEntity(
            userID=user.user_id,
            status=user.status,
            explicitWebauthnID=user.explicit_webauthn_id,
            fullName=user.full_name,
        )
