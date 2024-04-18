from abc import ABC, abstractmethod

from corbado_python_sdk.entities.user_entity import UserEntity


class SessionInterface(ABC):
    """
    SessionInterface for managing sessions.
    """

    # EmailOTPService
    @abstractmethod
    def get_short_session_value(self) -> str:
        """
        Returns the short-term session value from the cookie or the Authorization header.

        Returns:
            str: The short-term session value.
        """
        pass

    @abstractmethod
    def validate_short_session_value(self, value: str):
        """
        Validates the given short-term session value.

        Args:
            value (str): The value (JWT) to validate.

        Returns:
            Optional[Decoded]: Returns Decoded object on success, otherwise None.
        """
        pass

    @abstractmethod
    def get_last_short_session_validation_result(self) -> str:
        """
        Returns the last short-term session validation result.

        Returns:
            str: The last short-term session validation result.
        """
        pass

    @abstractmethod
    def get_current_user(self) -> UserEntity:
        """
        Returns the current user from the short-term session.

        Returns:
            UserEntity: The current user.
        """
        pass

    @abstractmethod
    def extract_bearer_token(self, authorization_header: str) -> str:
        """
        Extracts the bearer token from the authorization header.

        Args:
            authorization_header (str): The authorization header.

        Returns:
            str: The bearer token.
        """
        pass
