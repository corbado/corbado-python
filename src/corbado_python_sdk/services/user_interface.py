from abc import ABC, abstractmethod
from typing import Optional

from corbado_python_sdk.generated.models.generic_rsp import GenericRsp
from corbado_python_sdk.generated.models.user_create_req import UserCreateReq
from corbado_python_sdk.generated.models.user_create_rsp import UserCreateRsp
from corbado_python_sdk.generated.models.user_delete_req import UserDeleteReq
from corbado_python_sdk.generated.models.user_get_rsp import UserGetRsp
from corbado_python_sdk.generated.models.user_list_rsp import UserListRsp


class UserInterface(ABC):
    """Interface containing functions for interaction with users"""

    @abstractmethod
    def create(self, request: UserCreateReq) -> UserCreateRsp:
        """Creates a user

        Args:
            request (UserCreateReq): User create request

        Returns:
            UserCreateRsp: Response
        """
        pass

    @abstractmethod
    def get(self, user_id: str, remote_addr: str, user_agent: str) -> UserGetRsp:
        """Get user

        Args:
            user_id (str): User Id
            remote_addr (str): Remote address
            user_agent (str): User agent

        Returns:
            UserGetRsp: Response
        """
        pass

    @abstractmethod
    def delete(self, user_id: str, request: UserDeleteReq) -> GenericRsp:
        """Delete user

        Args:
            user_id (str): User ID
            request (UserDeleteReq): Request

        Returns:
            GenericRsp: Response
        """
        pass

    @abstractmethod
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
        pass
