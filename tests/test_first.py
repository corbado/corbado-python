import unittest
import json

from generated.configuration import Configuration
from generated.api_client import ApiClient
from generated.api.user_api import UserApi
from generated.models.user_list_rsp import UserListRsp
from generated.models.user_create_req import UserCreateReq
from generated.models.user_create_rsp import UserCreateRsp
from generated.exceptions import BadRequestException


class TestAuthMethod(unittest.TestCase):
    backendAPI = "https://backendapi.corbado.io"
    shortSessionCookieName = "cbo_short_session"

    """AuthMethod unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAuthMethod(self):

        # TODO: add username/password through env. variables
        conf = Configuration(
            username="",
            password="",
        )
        client = ApiClient(
            configuration=conf,
        )
        userApi = UserApi(api_client=client)
        ret: UserListRsp = userApi.user_list()
        print("Getting Users")
        for user in ret.data.users:
            print(
                f"Name: {user.full_name}, Email: {user.emails[0].email}, Creation Date: {user.created}"
            )

        create_request = UserCreateReq(
            name="FullNameCreate",
            fullName="CreateRequestTestName",
            email="test3@python.com",
        )
        print("Creating existing client")
        try:
            create_response: UserCreateRsp = userApi.user_create(
                user_create_req=create_request
            )
            print(f"Create response: {create_response}")
        except BadRequestException as e:
            print("Exception type:", type(e))
            data = json.loads(e.body)

            print(
                "Exception message:",
                data.get("error", {}).get("validation", [])[0].get("message", {}),
            )

        pass


if __name__ == "__main__":
    unittest.main()
