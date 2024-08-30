from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing_extensions import Annotated, Optional

from corbado_python_sdk.entities import UserEntity
from corbado_python_sdk.exceptions.server_exception import ServerException
from corbado_python_sdk.generated.api import UsersApi
from corbado_python_sdk.generated.exceptions import ApiException
from corbado_python_sdk.generated.models import UserCreateReq
from corbado_python_sdk.generated.models.user import User
from corbado_python_sdk.generated.models.user_status import UserStatus


class UserService(
    BaseModel,
):
    """Service for managing users."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    client: UsersApi

    def create_from_request(self, request: UserCreateReq) -> UserEntity:
        """Create a user from UserCreateReq.

        Args:
            request (UserCreateReq):  User create request

        Raises:
            ServerException: If any server side error occurs.

        Returns:
            UserEntity: _description_
        """
        try:
            user: User = self.client.user_create(user_create_req=request)
        except ApiException as e:
            raise ServerException(e)

        return UserEntity.from_user(user)

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
        request = UserCreateReq(status=status, fullName=full_name, explicitWebauthnID=explicit_webauthn_id)
        try:
            user: User = self.client.user_create(user_create_req=request)
        except ApiException as e:
            raise ServerException(e)

        return UserEntity.from_user(user)

    def get(self, user_id: Annotated[StrictStr, Field(description="ID of user")]) -> UserEntity:
        """Retrieve user from userId.

        Args:
            user_id (Annotated[StrictStr, Field, optional): UserId.)].

        Raises:
            ServerException:  If any server side error occurs.

        Returns:
            UserEntity: UserEntity.
        """
        try:
            user: User = self.client.user_get(user_id=user_id)
        except ApiException as e:
            raise ServerException(e)

        return UserEntity.from_user(user)

    def delete(self, user_id: str) -> None:
        """Delete user. Does not return anything. Throw if any error occurs (Like user not exists).

        Args:
            user_id (str): UserId.

        Raises:
            ServerException: If any server side error occurs.
        """
        try:
            self.client.user_delete(user_id=user_id)
        except ApiException as e:
            raise ServerException(e)
