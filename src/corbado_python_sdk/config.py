from pydantic import BaseModel, ConfigDict, field_validator


class Config(BaseModel):
    """Configuration class"""

    # Make sure that field assignments are also validated, use "config.model_config["validate_assignment"] =
    # False" to be able to use invalid assignments
    model_config = ConfigDict(validate_assignment=True)

    # Fields
    project_id: str
    api_secret: str
    frontend_api: str = ""
    backend_api: str = "https://backendapi.corbado.io"
    short_session_cookie_name: str = "cbo_short_session"

    # Field Validators
    @field_validator("project_id")
    @classmethod
    def project_id_validator(cls, project_id: str) -> str:
        """Field validator for project_ID

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
        """Field validator for api_secret

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

    # ------------ End validators --------------#
    def set_assignment_validation(self, validate: bool) -> None:
        """Only use it if you know what you do. Sets assignment validation.

        Args:
            validate (bool): Enable/disable validation
        """
        self.model_config["validate_assignment"] = validate
