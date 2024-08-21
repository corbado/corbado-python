from pydantic import BaseModel, Field
from typing_extensions import Optional


class SessionValidationResult(BaseModel):
    """Result class for SessionService validation."""

    authenticated: bool = Field(default=False, description="Indicates success of validation by session service.")
    user_id: Optional[str] = Field(default=None, description="The user ID.")
    full_name: Optional[str] = Field(default=None, description="The full name.")
