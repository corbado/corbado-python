from pydantic import ConfigDict

from corbado_python_sdk.generated.models.user import User


class UserEntity(User):
    """Represents a user entity."""

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @classmethod
    def from_user(cls, user: User) -> "UserEntity":
        """Create a UserEntity instance from a User.

        Args:
            user (User): User object

        Returns:
            UserEntity: UserEntity
        """
        return UserEntity(
            user_id=user.user_id,  # type: ignore
            status=user.status,
            explicit_webauthn_id=user.explicit_webauthn_id,  # type: ignore
            full_name=user.full_name,  # type: ignore
        )
