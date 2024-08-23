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

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from corbado_python_sdk.generated.models.error_rsp_all_of_error import ErrorRspAllOfError
from corbado_python_sdk.generated.models.request_data import RequestData
from typing import Optional, Set
from typing_extensions import Self

class ErrorRsp(BaseModel):
    """
    ErrorRsp
    """ # noqa: E501
    http_status_code: StrictInt = Field(description="HTTP status code of operation", alias="httpStatusCode")
    message: StrictStr
    request_data: RequestData = Field(alias="requestData")
    runtime: Union[StrictFloat, StrictInt] = Field(description="Runtime in seconds for this request")
    data: Optional[Dict[str, Any]] = None
    error: ErrorRspAllOfError
    __properties: ClassVar[List[str]] = ["httpStatusCode", "message", "requestData", "runtime", "data", "error"]

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
        """Create an instance of ErrorRsp from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of request_data
        if self.request_data:
            _dict['requestData'] = self.request_data.to_dict()
        # override the default output from pydantic by calling `to_dict()` of error
        if self.error:
            _dict['error'] = self.error.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ErrorRsp from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "httpStatusCode": obj.get("httpStatusCode"),
            "message": obj.get("message"),
            "requestData": RequestData.from_dict(obj["requestData"]) if obj.get("requestData") is not None else None,
            "runtime": obj.get("runtime"),
            "data": obj.get("data"),
            "error": ErrorRspAllOfError.from_dict(obj["error"]) if obj.get("error") is not None else None
        })
        return _obj


