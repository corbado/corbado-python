from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from corbado_python_sdk.entities import UserEntity
from corbado_python_sdk.exceptions.server_exception import ServerException
from corbado_python_sdk.exceptions.standard_exception import StandardException
from corbado_python_sdk.generated import ErrorRsp
from corbado_python_sdk.generated.api import UsersApi
from corbado_python_sdk.generated.exceptions import ApiException
from corbado_python_sdk.generated.models import (
    GenericRsp,
    UserCreateReq,
    UserCreateRsp,
    UserDeleteReq,
    UserGetRsp,
    UserListRsp,
)
from corbado_python_sdk.generated.models.user import User
from corbado_python_sdk.generated.models.user_status import UserStatus
from corbado_python_sdk.services.interface import UserInterface


class UserService(
    BaseModel,
    UserInterface,
):
    """Service for managing users."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    client: UsersApi

    def create(self, request: UserCreateReq) -> UserEntity:
        """Create an user.

        Args:
            request (UserCreateReq): User create request

        Raises:
            ServerException: If any server side error occurs.
        Returns:
            UserCreateRsp: Response
        """
        try:
            user: User = self.client.user_create(user_create_req=request)
        except ApiException as e:
            raise ServerException(e)

        return UserEntity.from_user(user)

    def list_users(
        self,
        remote_addr: Optional[str] = None,
        user_agent: Optional[str] = None,
        sort: Optional[str] = None,
        filter_args: Optional[List[str]] = None,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
    ) -> UserListRsp:
        """List users.

        Args:
            remote_addr (str): Remote address
            user_agent (str): User agent
            sort (str): sort
            filter_args (List[str]): Filter arguments
            page (int, optional): Page. Defaults to 1.
            page_size (int, optional): Page Size. Defaults to 10.

        Raises:
            ServerException: If any server side error occurs.
            StandardException: If an unexpected ErrorRsp is received.

        Returns:
            UserListRsp: Response
        """
        try:
            response: UserListRsp = self.client.user_list(
                user_agent=user_agent,
                remote_address=remote_addr,
                sort=sort,
                filter=filter_args,
                page=page,
                page_size=page_size,
            )
        except ApiException as e:
            raise ServerException(e)

        if isinstance(response, ErrorRsp):
            raise StandardException("Got unexpected ErrorRsp")

        return response

    def get(self, user_id: str, remote_addr: Optional[str] = None, user_agent: Optional[str] = None) -> UserGetRsp:
        """Get user.

        Args:
            user_id (str): User Id
            remote_addr (str): Remote address
            user_agent (str): User agent

        Raises:
            ServerException: If any server side error occurs.
            StandardException: If an unexpected ErrorRsp is received.

        Returns:
            UserGetRsp: Response
        """
        try:
            response: UserGetRsp = self.client.user_get(remote_address=remote_addr, user_agent=user_agent, user_id=user_id)
        except ApiException as e:
            raise ServerException(e)

        if isinstance(response, ErrorRsp):
            raise StandardException("Got unexpected ErrorRsp")

        return response

    def delete(self, user_id: str, request: UserDeleteReq) -> GenericRsp:
        """Delete user.

        Args:
            user_id (str): User ID
            request (UserDeleteReq): Request

        Raises:
            ServerException: If any server side error occurs.
            StandardException: If an unexpected ErrorRsp is received.

        Returns:
            GenericRsp: Response
        """
        try:
            response: GenericRsp = self.client.user_delete(user_delete_req=request, user_id=user_id)
        except ApiException as e:
            raise ServerException(e)

        if isinstance(response, ErrorRsp):
            raise StandardException("Got unexpected ErrorRsp")

        return response
