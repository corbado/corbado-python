from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing_extensions import Annotated, List, Optional

from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.generated import (
    ApiException,
    Identifier,
    IdentifierCreateReq,
    IdentifierList,
    IdentifiersApi,
    IdentifierStatus,
    IdentifierType,
    IdentifierUpdateReq,
)
from corbado_python_sdk.generated.models.paging import Paging
from corbado_python_sdk.services.interface.identifier_interface import (
    IdentifierInterface,
)


class IdentifierService(BaseModel, IdentifierInterface):
    """This class provides functionality for managing login identifiers."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    client: IdentifiersApi

    def create(
        self,
        user_id: Annotated[StrictStr, Field(description="ID of user")],
        identifier_type: IdentifierType,
        identifier_value: StrictStr,
        status: IdentifierStatus,
    ) -> Identifier:
        try:
            return self.client.identifier_create(
                user_id=user_id,
                identifier_create_req=IdentifierCreateReq(
                    identifierType=identifier_type, identifierValue=identifier_value, status=status
                ),
            )
        except ApiException as e:
            raise ServerException(e)

    def list(
        self,
        sort: Optional[StrictStr] = None,
        filters: Optional[List[StrictStr]] = None,
        page: StrictInt = 1,
        page_size: StrictInt = 10,
        user_id: Optional[StrictStr] = None,
        identifier_type: Optional[IdentifierType] = None,
    ) -> IdentifierList:
        if user_id:
            filters = filters or []
            if user_id.startswith("usr-"):
                user_id = user_id[4:]
            filters.append(f"userID:eq:{user_id}")
        if identifier_type:
            filters = filters or []
            filters.append(f"identifierType:eq:{identifier_type}")

        try:
            return self.client.identifier_list(sort=sort, filter=filters, page=page, page_size=page_size)
        except ApiException as e:
            raise ServerException(e)

    def list_all_identifiers_by_user_and_type(
        self,
        user_id: Annotated[StrictStr, Field(description="The user ID")],
        identifier_type: Optional[IdentifierType] = None,
        page: StrictInt = 1,
        page_size: StrictInt = 10,
    ) -> IdentifierList:
        return self.list(user_id=user_id, identifier_type=identifier_type, page=page, page_size=page_size)

    def list_all_emails_by_user_id(
        self,
        user_id: Annotated[StrictStr, Field(description="The user ID")],
    ) -> List[Identifier]:
        identifiers: List[Identifier] = []
        first_res: IdentifierList = self.list_all_identifiers_by_user_and_type(
            user_id=user_id, identifier_type=IdentifierType.EMAIL
        )
        identifiers.extend(first_res.identifiers)

        paging: Paging = first_res.paging
        while paging.page < paging.total_pages:
            paging.page += 1
            temp_res: IdentifierList = self.list_all_identifiers_by_user_and_type(
                user_id=user_id, identifier_type=IdentifierType.EMAIL, page=paging.page
            )
            identifiers.extend(temp_res.identifiers)

        return identifiers

    def exists_by_value_and_type(
        self,
        value: Annotated[StrictStr, Field(description="The identifier value")],
        identifier_type: IdentifierType,
    ) -> bool:
        try:
            filters: List[str] = [f"identifierValue:eq:{value}", f"identifierType:eq:{identifier_type}"]
            ret: IdentifierList = self.list(filters=filters)
            return bool(ret.identifiers)
        except ApiException as e:
            raise ServerException(e)

    def update_status(
        self,
        user_id: Annotated[StrictStr, Field(description="ID of user")],
        identifier_id: Annotated[StrictStr, Field(description="ID of login identifier")],
        status: IdentifierStatus,
    ) -> Identifier:
        try:
            identifier_update_req = IdentifierUpdateReq(status=status)
            return self.client.identifier_update(
                user_id=user_id, identifier_id=identifier_id, identifier_update_req=identifier_update_req
            )
        except ApiException as e:
            raise ServerException(e)
