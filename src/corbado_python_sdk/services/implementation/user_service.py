from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from corbado_python_sdk.exceptions.server_exception import ServerException
from corbado_python_sdk.generated.api.user_api import UserApi
from corbado_python_sdk.generated.exceptions import ApiException
from corbado_python_sdk.generated.models.generic_rsp import GenericRsp
from corbado_python_sdk.generated.models.user_create_req import UserCreateReq
from corbado_python_sdk.generated.models.user_create_rsp import UserCreateRsp
from corbado_python_sdk.generated.models.user_delete_req import UserDeleteReq
from corbado_python_sdk.generated.models.user_get_rsp import UserGetRsp
from corbado_python_sdk.generated.models.user_list_rsp import UserListRsp
from corbado_python_sdk.services.interface.user_interface import UserInterface
from corbado_python_sdk.utils import Util


class UserService(
    BaseModel,
    UserInterface,
):
    """Service for managing users"""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    client: UserApi

    def create(self, request: UserCreateReq) -> UserCreateRsp:
        """Creates an user

        Args:
            request (UserCreateReq): User create request

        Raises:
            ServerException: If any server side error occurs.

        Returns:
            UserCreateRsp: Response
        """

        try:
            response: UserCreateRsp = self.client.user_create(user_create_req=request)
        except ApiException as e:
            exception: ServerException = Util.convert_to_server_exception(e)
            raise exception

        return response

    def list_users(
        self,
        remote_addr: Optional[str] = None,
        user_agent: Optional[str] = None,
        sort: Optional[str] = None,
        filter_args: Optional[List[str]] = None,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
    ) -> UserListRsp:
        """List users

        Args:
            remote_addr (str): Remote address
            user_agent (str): User agent
            sort (str): sort
            filter_args (List[str]): Filter arguments
            page (int, optional): Page. Defaults to 1.
            page_size (int, optional): Page Size. Defaults to 10.

        Raises:
            ServerException: If any server side error occurs.

        Returns:
            UserListRsp: Response
        """
        try:
            responce = self.client.user_list(
                user_agent=user_agent,
                remote_address=remote_addr,
                sort=sort,
                filter=filter_args,
                page=page,
                page_size=page_size,
            )
        except ApiException as e:
            exception: ServerException = Util.convert_to_server_exception(e)
            raise exception

        return responce

    def get(self, user_id: str, remote_addr: Optional[str] = None, user_agent: Optional[str] = None) -> UserGetRsp:
        """Get user

        Args:
            user_id (str): User Id
            remote_addr (str): Remote address
            user_agent (str): User agent

        Raises:
            ServerException: If any server side error occurs.

        Returns:
            UserGetRsp: Response
        """
        try:
            responce: UserGetRsp = self.client.user_get(
                remote_address=remote_addr, user_agent=user_agent, user_id=user_id
            )
        except ApiException as e:
            exception: ServerException = Util.convert_to_server_exception(e)
            raise exception

        return responce

    def delete(self, user_id: str, request: UserDeleteReq) -> GenericRsp:
        """Delete user

        Args:
            user_id (str): User ID
            request (UserDeleteReq): Request

        Returns:
            GenericRsp: Response
        """
        try:
            responce: GenericRsp = self.client.user_delete(user_delete_req=request, user_id=user_id)
        except ApiException as e:
            exception: ServerException = Util.convert_to_server_exception(e)
            raise exception
        return responce
