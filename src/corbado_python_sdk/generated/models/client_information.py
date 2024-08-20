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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from corbado_python_sdk.generated.models.java_script_high_entropy import JavaScriptHighEntropy
from typing import Optional, Set
from typing_extensions import Self

class ClientInformation(BaseModel):
    """
    ClientInformation
    """ # noqa: E501
    remote_address: StrictStr = Field(description="Client's IP address", alias="remoteAddress")
    user_agent: StrictStr = Field(description="Client's user agent", alias="userAgent")
    client_env_handle: Optional[StrictStr] = Field(default=None, description="Client's environment handle", alias="clientEnvHandle")
    javascript_fingerprint: Optional[StrictStr] = Field(default=None, description="Client's fingerprint", alias="javascriptFingerprint")
    java_script_high_entropy: Optional[JavaScriptHighEntropy] = Field(default=None, alias="javaScriptHighEntropy")
    bluetooth_available: Optional[StrictBool] = Field(default=None, description="Client's Bluetooth availability", alias="bluetoothAvailable")
    password_manager_available: Optional[StrictBool] = Field(default=None, description="Client's password manager availability", alias="passwordManagerAvailable")
    user_verifying_platform_authenticator_available: StrictBool = Field(alias="userVerifyingPlatformAuthenticatorAvailable")
    __properties: ClassVar[List[str]] = ["remoteAddress", "userAgent", "clientEnvHandle", "javascriptFingerprint", "javaScriptHighEntropy", "bluetoothAvailable", "passwordManagerAvailable", "userVerifyingPlatformAuthenticatorAvailable"]

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
        """Create an instance of ClientInformation from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of java_script_high_entropy
        if self.java_script_high_entropy:
            _dict['javaScriptHighEntropy'] = self.java_script_high_entropy.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ClientInformation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "remoteAddress": obj.get("remoteAddress"),
            "userAgent": obj.get("userAgent"),
            "clientEnvHandle": obj.get("clientEnvHandle"),
            "javascriptFingerprint": obj.get("javascriptFingerprint"),
            "javaScriptHighEntropy": JavaScriptHighEntropy.from_dict(obj["javaScriptHighEntropy"]) if obj.get("javaScriptHighEntropy") is not None else None,
            "bluetoothAvailable": obj.get("bluetoothAvailable"),
            "passwordManagerAvailable": obj.get("passwordManagerAvailable"),
            "userVerifyingPlatformAuthenticatorAvailable": obj.get("userVerifyingPlatformAuthenticatorAvailable")
        })
        return _obj


