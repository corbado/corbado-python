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
        """Create a new identifier for the given user.

        Args:
            user_id (StrictStr): The ID of the user to whom the identifier will be assigned.
            identifier_type (IdentifierType): The type of identifier to create (e.g., email, phone).
            identifier_value (StrictStr): The value of the identifier (e.g., the email address or phone number).
            status (IdentifierStatus): The status of the identifier (e.g., active, inactive).

        Raises:
            ServerException: If there is an error from the API server.

        Returns:
            Identifier: The created identifier object.
        """
        pass

    @abstractmethod
    def list_identifiers(
        self,
        sort: Optional[StrictStr] = None,
        filters: Optional[List[StrictStr]] = None,
        page: StrictInt = 1,
        page_size: StrictInt = 10,
        user_id: Optional[StrictStr] = None,
        identifier_type: Optional[IdentifierType] = None,
        identifier_value: Optional[StrictStr] = None,
    ) -> IdentifierList:
        """List identifiers with optional filters and pagination.

        Args:
            sort (Optional[StrictStr], optional): The sorting order for the results (e.g., 'createdAt:desc'). Defaults to None.
            filters (Optional[List[StrictStr]], optional): A list of filters to
                apply to the results (e.g., 'status:eq:active'). Defaults to None.
            page (StrictInt): The page number for pagination. Defaults to 1.
            page_size (StrictInt): The number of results per page. Defaults to 10.
            user_id (Optional[StrictStr], optional): Filter results by user ID. Defaults to None.
            identifier_type (Optional[IdentifierType], optional): Filter results by identifier type. Defaults to None.
            identifier_value (Optional[StrictStr], optional): Filter results by identifier value. Defaults to None.

        Raises:
            ServerException: If there is an error from the API server.

        Returns:
            IdentifierList: A list of identifiers that match the criteria.
        """
        pass

    @abstractmethod
    def list_all_emails_by_user_id(
        self,
        user_id: Annotated[StrictStr, Field(description="The user ID")],
    ) -> List[Identifier]:
        """Retrieve all email identifiers for a specific user, handling pagination.

        Args:
            user_id (StrictStr): The ID of the user whose email identifiers are to be listed.

        Returns:
            List[Identifier]: A list of email identifiers associated with the user.
        """
        pass

    @abstractmethod
    def exists_by_value_and_type(
        self,
        value: Annotated[StrictStr, Field(description="The identifier value")],
        identifier_type: IdentifierType,
    ) -> bool:
        """Check if an identifier with a specific value and type exists.

        Args:
            value (StrictStr): The value of the identifier to check (e.g., an email address or phone number).
            identifier_type (IdentifierType): The type of identifier to check (e.g., email, phone).

        Raises:
            ServerException: If there is an error from the API server.

        Returns:
            bool: True if the identifier exists, False otherwise.
        """
        pass

    @abstractmethod
    def update_status(
        self,
        user_id: Annotated[StrictStr, Field(description="ID of user")],
        identifier_id: Annotated[StrictStr, Field(description="ID of login identifier")],
        status: IdentifierStatus,
    ) -> Identifier:
        """Update the status of a specific identifier.

        Args:
            user_id (StrictStr): The ID of the user to whom the identifier belongs.
            identifier_id (StrictStr): The ID of the identifier to update.
            status (IdentifierStatus): The new status for the identifier (e.g., active, inactive).

        Raises:
            ServerException: If there is an error from the API server.

        Returns:
            Identifier: The updated identifier object.
        """
        pass

    @abstractmethod
    def delete(
        self,
        user_id: StrictStr,
        identifier_id: StrictStr,
    ):
        """Delete the identifier.

        Args:
            user_id (StrictStr): ID of user.
            identifier_id (StrictStr): ID of login identifier.

        Raises:
            ServerException: _description_

        """
        pass
