from abc import ABC, abstractmethod

from corbado_python_sdk.entities.user_entity import UserEntity


class SessionInterface(ABC):
    """
    SessionInterface for managing sessions.
    """

    @abstractmethod
    def validate_short_session_value(self, short_session: str) -> UserEntity:
        """
        Validates the given short-term session value.

        Args:
            value (str): The value (JWT) to validate.

        Returns:
            Optional[Decoded]: Returns Decoded object on success, otherwise None.
        """
        pass

    @abstractmethod
    def get_current_user(self, short_session: str) -> UserEntity:
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
