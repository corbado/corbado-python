from pydantic import BaseModel
from user_interface import UserInterface

from ..generated.models.user_create_req import UserCreateReq
from ..generated.models.user_create_rsp import UserCreateRsp


class UserService(
    BaseModel,
    UserInterface,
):
    temp: str = ""

    def create(self, req: UserCreateReq) -> UserCreateRsp:
        return super().create(req)
