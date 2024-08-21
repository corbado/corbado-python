from abc import ABC, abstractmethod

from pydantic import Field, StrictInt, StrictStr
from typing_extensions import Annotated, List, Optional

from corbado_python_sdk.generated import (
    Identifier,
    IdentifierList,
    IdentifierStatus,
    IdentifierType,
)


class IdentifierInterface(ABC):
    """This class provides functionality for managing login identifiers."""

    @abstractmethod
    def create(
        self,
        user_id: Annotated[StrictStr, Field(description="ID of user")],
        identifier_type: IdentifierType,
        identifier_value: StrictStr,
        status: IdentifierStatus,
    ) -> Identifier:
        pass

    @abstractmethod
    def list(
        self,
        sort: Optional[StrictStr] = None,
        filters: Optional[List[StrictStr]] = None,
        page: StrictInt = 1,
        page_size: StrictInt = 10,
        user_id: Optional[StrictStr] = None,
        identifier_type: Optional[IdentifierType] = None,
    ) -> IdentifierList:
        pass

    @abstractmethod
    def list_all_identifiers_by_user_and_type(
        self,
        user_id: Annotated[StrictStr, Field(description="The user ID")],
        identifier_type: Optional[IdentifierType] = None,
        page: StrictInt = 1,
        page_size: StrictInt = 10,
    ) -> IdentifierList:
        pass

    @abstractmethod
    def list_all_emails_by_user_id(
        self,
        user_id: Annotated[StrictStr, Field(description="The user ID")],
    ) -> List[Identifier]:
        pass

    @abstractmethod
    def exists_by_value_and_type(
        self,
        value: Annotated[StrictStr, Field(description="The identifier value")],
        identifier_type: IdentifierType,
    ) -> bool:
        pass

    @abstractmethod
    def update_status(
        self,
        user_id: Annotated[StrictStr, Field(description="ID of user")],
        identifier_id: Annotated[StrictStr, Field(description="ID of login identifier")],
        status: IdentifierStatus,
    ) -> Identifier:
        pass
