from generated.models.user_create_req import UserCreateReq
from generated.models.user_create_rsp import UserCreateRsp
from generated.models.user_list_rsp import UserListRsp
from pydantic import BaseModel
from user_interface import UserInterface

from ..generated.api.user_api import UserApi


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

    def list(
        self, remote_addr: str, user_agent: str, sort: str, filter_args: list[str], page: int = 1, page_size: int = 10
    ) -> UserListRsp:
        return self.client.user_list(
            user_agent=user_agent,
            remote_address=remote_addr,
            sort=sort,
            filter=filter_args,
            page=page,
            page_size=page_size,
        )
