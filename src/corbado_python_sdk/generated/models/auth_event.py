# coding: utf-8

"""
    Corbado Backend API

     # Introduction This documentation gives an overview of all Corbado Backend API calls to implement passwordless authentication with Passkeys. 

    The version of the OpenAPI document: 2.0.0
    Contact: support@corbado.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List
from corbado_python_sdk.generated.models.auth_event_method import AuthEventMethod
from corbado_python_sdk.generated.models.auth_event_status import AuthEventStatus
from corbado_python_sdk.generated.models.auth_event_type import AuthEventType
from typing import Optional, Set
from typing_extensions import Self

class AuthEvent(BaseModel):
    """
    AuthEvent
    """ # noqa: E501
    auth_event_id: StrictStr = Field(alias="authEventID")
    user_id: StrictStr = Field(description="ID of the user", alias="userID")
    username: StrictStr
    event_type: AuthEventType = Field(alias="eventType")
    method: AuthEventMethod
    created: StrictStr = Field(description="Timestamp of when the entity was created in yyyy-MM-dd'T'HH:mm:ss format")
    created_ms: StrictInt = Field(alias="createdMs")
    status: AuthEventStatus
    __properties: ClassVar[List[str]] = ["authEventID", "userID", "username", "eventType", "method", "created", "createdMs", "status"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of AuthEvent from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AuthEvent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "authEventID": obj.get("authEventID"),
            "userID": obj.get("userID"),
            "username": obj.get("username"),
            "eventType": obj.get("eventType"),
            "method": obj.get("method"),
            "created": obj.get("created"),
            "createdMs": obj.get("createdMs"),
            "status": obj.get("status")
        })
        return _obj


