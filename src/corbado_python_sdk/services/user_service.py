from pydantic import BaseModel
from src.corbado_python_sdk.generated.models.user_create_req import UserCreateReq
from src.corbado_python_sdk.generated.models.user_create_rsp import UserCreateRsp
from user_interface import UserInterface


class UserService(BaseModel, UserInterface):
    temp: str = ""

    def create(self, req: UserCreateReq) -> UserCreateRsp:
        # TODO: complete
        return super().create(req)
