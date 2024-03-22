from abc import ABC, abstractmethod

from ..generated.models.user_create_req import UserCreateReq
from ..generated.models.user_create_rsp import UserCreateRsp


class UserInterface(ABC):

    @abstractmethod
    def create(self, req: UserCreateReq) -> UserCreateRsp:
        pass

    # TODO complete interface
