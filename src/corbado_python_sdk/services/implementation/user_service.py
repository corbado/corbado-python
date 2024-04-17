from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from corbado_python_sdk.generated.api.user_api import UserApi
from corbado_python_sdk.generated.models.generic_rsp import GenericRsp
from corbado_python_sdk.generated.models.user_create_req import UserCreateReq
from corbado_python_sdk.generated.models.user_create_rsp import UserCreateRsp
from corbado_python_sdk.generated.models.user_delete_req import UserDeleteReq
from corbado_python_sdk.generated.models.user_get_rsp import UserGetRsp
from corbado_python_sdk.generated.models.user_list_rsp import UserListRsp

from ..interface.user_interface import UserInterface


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

        Returns:
            UserCreateRsp: Response
        """
        response: UserCreateRsp = self.client.user_create(user_create_req=request)
        print(f"{response.http_status_code}")
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

        Returns:
            UserListRsp: Response
        """

        print("listing users")
        return self.client.user_list(
            user_agent=user_agent,
            remote_address=remote_addr,
            sort=sort,
            filter=filter_args,
            page=page,
            page_size=page_size,
        )

    def get(
        self, user_id: Optional[str] = None, remote_addr: Optional[str] = None, user_agent: Optional[str] = None
    ) -> UserGetRsp:
        """Get user

        Args:
            user_id (str): User Id
            remote_addr (str): Remote address
            user_agent (str): User agent

        Returns:
            UserGetRsp: Response
        """
        return self.client.user_get(remote_address=remote_addr, user_agent=user_agent, user_id=user_id)

    def delete(self, user_id: str, request: UserDeleteReq) -> GenericRsp:
        """Delete user

        Args:
            user_id (str): User ID
            request (UserDeleteReq): Request

        Returns:
            GenericRsp: Response
        """
        return self.client.user_delete(user_delete_req=request, user_id=user_id)
