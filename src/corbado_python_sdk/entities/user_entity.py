from pydantic import ConfigDict

from corbado_python_sdk.generated.models.user import User


class UserEntity(User):
    """Represents a user entity."""

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
