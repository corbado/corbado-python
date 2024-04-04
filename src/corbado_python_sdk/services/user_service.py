from typing import Optional

from pydantic import BaseModel

from corbado_python_sdk.generated.api.user_api import UserApi
from corbado_python_sdk.generated.models.user_create_req import UserCreateReq
from corbado_python_sdk.generated.models.user_create_rsp import UserCreateRsp
from corbado_python_sdk.generated.models.user_list_rsp import UserListRsp

from .user_interface import UserInterface


class UserService(
    BaseModel,
    UserInterface,
):
    """Service for managing users"""

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
        remote_addr: str,
        user_agent: str,
        sort: str,
        filter_args: list[str],
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
    ) -> UserListRsp:
        """List users

        Args:
            remote_addr (str): Remote address
            user_agent (str): User agent
            sort (str): sort
            filter_args (list[str]): Filter arguments
            page (int, optional): Page. Defaults to 1.
            page_size (int, optional): Page Size. Defaults to 10.

        Returns:
            UserListRsp: Response
        """
        return self.client.user_list(
            user_agent=user_agent,
            remote_address=remote_addr,
            sort=sort,
            filter=filter_args,
            page=page,
            page_size=page_size,
        )
