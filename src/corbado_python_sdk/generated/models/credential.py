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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List
from corbado_python_sdk.generated.models.aaguid_details import AaguidDetails
from typing import Optional, Set
from typing_extensions import Self

class Credential(BaseModel):
    """
    Credential
    """ # noqa: E501
    id: StrictStr
    credential_id: StrictStr = Field(alias="credentialID")
    attestation_type: StrictStr = Field(alias="attestationType")
    transport: List[StrictStr]
    backup_eligible: StrictBool = Field(alias="backupEligible")
    backup_state: StrictBool = Field(alias="backupState")
    authenticator_aaguid: StrictStr = Field(alias="authenticatorAAGUID")
    source_os: StrictStr = Field(alias="sourceOS")
    source_browser: StrictStr = Field(alias="sourceBrowser")
    last_used: StrictStr = Field(description="Timestamp of when the passkey was last used in yyyy-MM-dd'T'HH:mm:ss format", alias="lastUsed")
    last_used_ms: StrictInt = Field(alias="lastUsedMs")
    created: StrictStr = Field(description="Timestamp of when the entity was created in yyyy-MM-dd'T'HH:mm:ss format")
    created_ms: StrictInt = Field(alias="createdMs")
    status: StrictStr = Field(description="Status")
    aaguid_details: AaguidDetails = Field(alias="aaguidDetails")
    __properties: ClassVar[List[str]] = ["id", "credentialID", "attestationType", "transport", "backupEligible", "backupState", "authenticatorAAGUID", "sourceOS", "sourceBrowser", "lastUsed", "lastUsedMs", "created", "createdMs", "status", "aaguidDetails"]

    @field_validator('transport')
    def transport_validate_enum(cls, value):
        """Validates the enum"""
        for i in value:
            if i not in set(['usb', 'nfc', 'ble', 'internal', 'hybrid', 'smart-card']):
                raise ValueError("each list item must be one of ('usb', 'nfc', 'ble', 'internal', 'hybrid', 'smart-card')")
        return value

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['pending', 'active']):
            raise ValueError("must be one of enum values ('pending', 'active')")
        return value

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
        """Create an instance of Credential from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of aaguid_details
        if self.aaguid_details:
            _dict['aaguidDetails'] = self.aaguid_details.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Credential from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "credentialID": obj.get("credentialID"),
            "attestationType": obj.get("attestationType"),
            "transport": obj.get("transport"),
            "backupEligible": obj.get("backupEligible"),
            "backupState": obj.get("backupState"),
            "authenticatorAAGUID": obj.get("authenticatorAAGUID"),
            "sourceOS": obj.get("sourceOS"),
            "sourceBrowser": obj.get("sourceBrowser"),
            "lastUsed": obj.get("lastUsed"),
            "lastUsedMs": obj.get("lastUsedMs"),
            "created": obj.get("created"),
            "createdMs": obj.get("createdMs"),
            "status": obj.get("status"),
            "aaguidDetails": AaguidDetails.from_dict(obj["aaguidDetails"]) if obj.get("aaguidDetails") is not None else None
        })
        return _obj


