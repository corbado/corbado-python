from pydantic import BaseModel, Field
from typing_extensions import Optional

from corbado_python_sdk.exceptions.standard_exception import StandardException

NO_AUTH = "User is not authenticated"


class UserEntity(BaseModel):
    """
    Represents a user entity.

    Attributes:
        authenticated (bool): Indicates if the user is authenticated.
        id (str): User ID.
        name (str): User name.
        email (str): User email.
        phoneNumber (str): User phone number.
    """

    authenticated: bool
    _user_id: str = ""
    _name: str = ""
    _email: str = ""
    _phone_number: str = ""

    # Interfaces
    @property
    def user_id(self) -> str:
        """Get user user_id.

        Returns:
            user_id (str): User id.

        Raises:
            StandardException: If the user is not authenticated.
        """
        if not self.authenticated or not self._user_id:
            raise StandardException(NO_AUTH)
        return self._user_id

    @property
    def name(self) -> str:
        """Get user name.

        Returns:
            name (str): User name.

        Raises:
            StandardException: If the user is not authenticated.
        """
        if not self.authenticated or not self._name:
            raise StandardException(NO_AUTH)
        return self._name

    @property
    def email(self) -> str:
        """Get user E-mail.

        Returns:
            name (str): User E-mail.

        Raises:
            StandardException: If the user is not authenticated.
        """
        if not self.authenticated or not self._email:
            raise StandardException(NO_AUTH)
        return self._email

    @property
    def phone_number(self) -> str:
        """Get user phone number.

        Returns:
            name (str): User phone number.

        Raises:
            StandardException: If the user is not authenticated.
        """
        if not self.authenticated or not self._phone_number:
            raise StandardException(NO_AUTH)
        return self._phone_number

    @classmethod
    def create_authenticated_user(
        cls, user_id: str = "", name: str = "", email: str = "", phone_number: str = ""
    ) -> "UserEntity":
        """Constructor for authenticated user.

        Args:
            user_id (str, optional): user_id. Defaults to "".
            name (str, optional): name. Defaults to "".
            email (str, optional): email. Defaults to "".
            phone_number (str, optional): phone_number. Defaults to "".

        Returns:
            UserEntity: User Entity
        """
        user = UserEntity(authenticated=True)
        user._email = email
        user._user_id = user_id
        user._name = name
        user._phone_number = phone_number
        return user
