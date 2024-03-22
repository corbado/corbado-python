from pydantic import BaseModel, ConfigDict, field_validator, ValidationError
from pydantic_core import ErrorDetails


class Config(BaseModel):
    # Make sure that field assignments are also validated, use "config.model_config["validate_assignment"] =
    # False" to be able to use invalid assignments
    model_config = ConfigDict(validate_assignment=True)

    # Fields
    project_id: str
    api_secret: str
    test_p: str = ""
    frontend_api: str = ""
    backend_api: str = "https://backendapi.corbado.io"
    short_session_cookie_name: str = "cbo_short_session"

    # Field Validators
    @field_validator("project_ID")
    @classmethod
    def project_id_validator(cls, project_id: str) -> str:
        """Since project ID and API secret are always needed they must be
          passed during initialization.

        Args:
            project_id (str): Project ID

        Raises:
            ValueError: is thrown if project ID does not start with "pro-"

        Returns:
            str: validated project_id
        """
        if not project_id.startswith("pro-"):
            raise ValueError(
                f'Invalid project ID "{project_id}" given, needs to start with "pro-"'
            )
        return project_id

    @field_validator("api_secret")
    @classmethod
    def api_secret_must_start_with_corbado1(cls, api_secret: str) -> str:

        if not api_secret.startswith("corbado1_"):
            raise ValueError(
                f'Invalid API Secret "{api_secret}" given, needs to start with "corbado1_"'
            )

        return api_secret

    # ------------ End validators --------------#
    def set_assignment_validation(self, validate: bool) -> None:
        """Only use it if you know what you do. Sets assignment validation.

        Args:
            validate (bool): Enable/disable validation
        """
        self.model_config["validate_assignment"] = validate


# Example for error parsing:
try:
    config = Config(project_id="213 2", api_secret="123", test_p="te1")
except ValidationError as exc:
    errors: list[ErrorDetails] = exc.errors()
    for errs in errors:
        print(errs.get("msg"))
