from typing import Any, Dict, List, Optional


class ServerException(Exception):
    """
    Custom exception class for server-related errors.
    """

    def __init__(
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
        self.runtime: float | None = runtime
        self.error: Dict[str, Any] = error or {}

        validation_messages: List[str] = self.get_validation_messages()
        message += f' (HTTP status code: {http_status_code}, validation messages: {"; ".join(validation_messages)})'

        super().__init__(message)

    def get_validation_messages(self) -> List[str]:
        """Get the validation messages from the error information.

        Returns:
            List[str]: List of validation messages
        """
        validation: List[Dict[str, Any]] = self.error.get("validation", [])
        return [f"{item['field']}: {item['message']}" for item in validation]
