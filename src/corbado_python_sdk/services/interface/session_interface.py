from abc import ABC, abstractmethod

from corbado_python_sdk.entities.session_validation_result import (
    SessionValidationResult,
)


class SessionInterface(ABC):
    """SessionInterface for managing sessions."""

    @abstractmethod
    def get_and_validate_short_session_value(self, short_session: str) -> SessionValidationResult:
        """Validate  the given short-term session value.

        Args:
            short_session (str): The value (JWT) to validate.

        Returns:
            Optional[Decoded]: Returns Decoded object on success, otherwise None.
        """
        pass

    @abstractmethod
    def get_current_user(self, short_session: str) -> SessionValidationResult:
        """Return current user for the short session.

        Args:
            short_session (str): Short session.

        Returns:
            UserEntity:  UserEntity with authenticated=True on success, otherwise with authenticated=False.
        """
        pass
