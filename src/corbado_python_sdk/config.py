from typing import Optional

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator
from typing_extensions import Annotated

from corbado_python_sdk.utils import validators


class Config(BaseModel):
    """
    Configuration class for setting up project parameters.

    This class uses Pydantic's `BaseModel` to validate configuration parameters.
    Field assignments are validated by default to ensure that any new assignments
    adhere to the defined types and constraints. To disable this validation, set
    `set_assignment_validation(False)`.

    Attributes:
        project_id (str): The unique identifier for the project.
        api_secret (str): The secret key used to authenticate API requests.
        backend_api (str): The base URL for the backend API. Defaults to "https://backendapi.corbado.io".
        short_session_cookie_name (str): The name of the cookie for short session management. Defaults to "cbo_short_session".
    """

    # Make sure that field assignments are also validated, use "set_assignment_validation(False)"
    # to be able to use invalid assignments
    model_config = ConfigDict(validate_assignment=True)

    # Fields
    project_id: str
    api_secret: str
    backend_api: str = "https://backendapi.corbado.io"
    short_session_cookie_name: str = "cbo_short_session"

    _issuer: Optional[Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]] = None
    _frontend_api: Optional[str] = None

    # Field Validators
    _backend_api_validator = field_validator("backend_api")(validators.url_validator)

    @field_validator("project_id")
    @classmethod
    def project_id_validator(cls, project_id: str) -> str:
        """Field validator for project_ID.

        Args:
            project_id (str): project ID

        Raises:
            ValueError: Raises ValueError if project_id does not start with "pro-"

        Returns:
            str: validated project ID
        """
        if not project_id.startswith("pro-"):
            raise ValueError(f'Invalid project ID "{project_id}" given, needs to start with "pro-"')
        return project_id

    @field_validator("api_secret")
    @classmethod
    def api_secret_must_start_with_corbado1(cls, api_secret: str) -> str:
        """Field validator for api_secret.

        Args:
            api_secret (str): API secret

        Raises:
            ValueError: Raises ValueError if api_secret does not start with "corbado1_"

        Returns:
            str: validated API secret
        """
        if not api_secret.startswith("corbado1_"):
            raise ValueError(f'Invalid API Secret "{api_secret}" given, needs to start with "corbado1_"')
        return api_secret

    # --------- Properties ----------#
    @property
    def issuer(self) -> str:
        """Get issuer. By default issuer = frontend_api, but can be overridden.

        Returns:
            str: issuer.
        """
        if not self._issuer:
            self._issuer = self.frontend_api
        return self._issuer

    @issuer.setter
    def issuer(self, issuer: str) -> None:
        """Set issuer.

        Args:
            issuer (str): issuer to set.
        """
        self._issuer = issuer

    @property
    def frontend_api(self) -> str:
        """Get Frontend API.

        Returns:
            str: Frontend API
        """
        if not self._frontend_api:
            self._frontend_api = "https://" + self.project_id + ".frontendapi.corbado.io"
        return self._frontend_api

    @frontend_api.setter
    def frontend_api(self, frontend_api: str) -> None:
        """Set Frontend API. Use it to override default value.

        Args:
            frontend_api (str): Frontend API to set.
        """
        self._frontend_api = validators.url_validator(url=frontend_api)  # validate url

    # ------- Internal --------------#
    def set_assignment_validation(self, validate: bool) -> None:
        """Only use it if you know what you do. Sets assignment validation.

        Args:
            validate (bool): Enable/disable validation
        """
        self.model_config["validate_assignment"] = validate
