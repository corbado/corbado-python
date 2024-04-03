from abc import ABC, abstractmethod

from generated.models.generic_rsp import GenericRsp
from generated.models.user_create_req import UserCreateReq
from generated.models.user_create_rsp import UserCreateRsp
from generated.models.user_delete_req import UserDeleteReq
from generated.models.user_get_rsp import UserGetRsp
from generated.models.user_list_rsp import UserListRsp


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
        pass

    @abstractmethod
    def delete(self, user_id: str, request: UserDeleteReq) -> GenericRsp:
        pass

    @abstractmethod
    def list(
        self, remote_addr: str, user_agent: str, sort: str, filter_args: list[str], page: int = 1, page_size: int = 10
    ) -> UserListRsp:
        pass


# public function delete(string $id, UserDeleteReq $req): GenericRsp;

# public function get(string $id, string $remoteAddr = '', string $userAgent = ''): UserGetRsp;
# public function list(string $remoteAddr = '', string $userAgent = '', string $sort = '', array $filter = [], int $page = 1, int $pageSize = 10): UserListRsp;
