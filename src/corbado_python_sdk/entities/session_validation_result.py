from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Optional


class SessionValidationResult(BaseModel):
    """Result class for SessionService validation."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    authenticated: bool = Field(default=False, description="Indicates success of validation by session service.")
    user_id: Optional[str] = Field(default=None, description="The user ID.")
    full_name: Optional[str] = Field(default=None, description="The full name.")
    error: Optional[Exception] = Field(default=None, description="Error occurred during validation.")
