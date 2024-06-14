from typing import Any, Dict, List, Optional

from corbado_python_sdk.exceptions.standard_exception import StandardException
from corbado_python_sdk.generated import ApiException

from ..utils.util import Util


class ServerException(Exception):
    """Custom exception class for server-related errors."""

    def __init__(self, e: ApiException) -> None:
        """Convert ApiException to ServerException.

        Args:
            e (ApiException): Exception to be converted.

        Raises:
            StandardException: If response body is not a string.

        """
        __body = e.body
        if not isinstance(__body, str):
            raise StandardException("Response body is not a string")
        __data: Dict[str, Any] = Util.json_decode(__body)
        self.__initialize(
            http_status_code=__data["httpStatusCode"],
            message=__data["message"],
            request_data=__data["requestData"],
            runtime=__data["runtime"],
            error=__data["error"],
        )

    def __initialize(
        self,
        http_status_code: int,
        message: str,
        request_data: Optional[Dict[str, Any]] = None,
        runtime: Optional[float] = None,
        error: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize ServerException with specific attributes.

        Args:
            http_status_code (int):  HTTP status code associated with the error
            message (str): Error message
            request_data (Optional[Dict[str, Any]], optional): Additional data associated with the request (optional)
            runtime (Optional[float], optional): Runtime information (optional). Defaults to None.
            error (Optional[Dict[str, Any]], optional): Specific error information (optional). Defaults to None.
        """
        self.http_status_code: int = http_status_code
        self.request_data: Dict[str, Any] = request_data or {}
        self.runtime: Optional[float] = runtime
        self.error: Dict[str, Any] = error or {}
        self.error_type: str = self.error.get("type", "")

        self.validation_messages: List[str] = self._get_validation_messages()
        message += (
            f' (HTTP status code: {http_status_code}, validation messages: {"; ".join(self.validation_messages)})'
        )

        super().__init__(message)

    def _get_validation_messages(self) -> List[str]:
        """Get the validation messages from the error information.

        Returns:
            List[str]: List of validation messages
        """
        validation: List[Dict[str, Any]] = self.error.get("validation", [])
        return [f"{item['field']}: {item['message']}" for item in validation]

    @property
    def request_id(self) -> str:
        """Get request ID.

        Returns:
            str: Request ID.
        """
        return self.request_data.get("requestID") or ""
