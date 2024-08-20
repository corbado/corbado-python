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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List
from corbado_python_sdk.generated.models.paging import Paging
from corbado_python_sdk.generated.models.passkey_challenge import PasskeyChallenge
from typing import Optional, Set
from typing_extensions import Self

class PasskeyChallengeList(BaseModel):
    """
    PasskeyChallengeList
    """ # noqa: E501
    passkey_challenges: List[PasskeyChallenge] = Field(alias="passkeyChallenges")
    paging: Paging
    __properties: ClassVar[List[str]] = ["passkeyChallenges", "paging"]

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
        """Create an instance of PasskeyChallengeList from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in passkey_challenges (list)
        _items = []
        if self.passkey_challenges:
            for _item_passkey_challenges in self.passkey_challenges:
                if _item_passkey_challenges:
                    _items.append(_item_passkey_challenges.to_dict())
            _dict['passkeyChallenges'] = _items
        # override the default output from pydantic by calling `to_dict()` of paging
        if self.paging:
            _dict['paging'] = self.paging.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PasskeyChallengeList from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "passkeyChallenges": [PasskeyChallenge.from_dict(_item) for _item in obj["passkeyChallenges"]] if obj.get("passkeyChallenges") is not None else None,
            "paging": Paging.from_dict(obj["paging"]) if obj.get("paging") is not None else None
        })
        return _obj


