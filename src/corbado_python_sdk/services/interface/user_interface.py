from abc import ABC, abstractmethod

from pydantic import Field, StrictStr
from typing_extensions import Annotated, Optional

from corbado_python_sdk.entities import UserEntity
from corbado_python_sdk.generated.models import UserCreateReq
from corbado_python_sdk.generated.models.user_status import UserStatus


class UserInterface(ABC):
    """Interface containing functions for interaction with users."""

    @abstractmethod
    def create_from_request(self, request: UserCreateReq) -> UserEntity:
        """Create a user from UserCreateReq.

        Args:
            request (UserCreateReq):  User create request

        Raises:
            ServerException: If any server side error occurs.

        Returns:
            UserEntity: _description_
        """

    @abstractmethod
    def create(
        self,
        status: UserStatus,
        full_name: Optional[StrictStr] = None,
        explicit_webauthn_id: Optional[StrictStr] = None,
    ) -> UserEntity:
        """Create a user.

        Args:
            status (UserStatus): User status.
            full_name (Optional[StrictStr], optional): Full name. Defaults to None.
            explicit_webauthn_id (Optional[StrictStr], optional): explicit_webauthn_id. Defaults to None.

        Raises:
            ServerException:  If any server side error occurs.

        Returns:
            UserEntity: UserEntity.
        """

    @abstractmethod
    def get(self, user_id: Annotated[StrictStr, Field(description="ID of user")]) -> UserEntity:
        """Retrieve user from userId.

        Args:
            user_id (Annotated[StrictStr, Field, optional): UserId.)].

        Raises:
            ServerException:  If any server side error occurs.

        Returns:
            UserEntity: UserEntity.
        """

    @abstractmethod
    def delete(self, user_id: str):
        """Delete user. Does not return anything. Throw if any error occurs (Like user not exists).

        Args:
            user_id (str): UserId.

        Raises:
            ServerException: If any server side error occurs.
        """
