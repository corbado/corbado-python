from abc import ABC, abstractmethod
from typing import List, Optional

from corbado_python_sdk.generated.models import (
    GenericRsp,
    UserCreateReq,
    UserCreateRsp,
    UserDeleteReq,
    UserGetRsp,
    UserListRsp,
)


class UserInterface(ABC):
    """Interface containing functions for interaction with users."""

    @abstractmethod
    def create(self, request: UserCreateReq) -> UserCreateRsp:
        """Create a user.

        Args:
            request (UserCreateReq): User create request

        Returns:
            UserCreateRsp: Response
        """
        pass

    @abstractmethod
    def get(self, user_id: str, remote_addr: Optional[str] = None, user_agent: Optional[str] = None) -> UserGetRsp:
        """Get user.

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
        """Delete user.

        Args:
            user_id (str): User ID
            request (UserDeleteReq): Request

        Returns:
            GenericRsp: Response
        """
        pass

    @abstractmethod
    # name 'list()' would shadow the python's builtin 'list'
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

        Returns:
            UserListRsp: Response
        """
        pass
