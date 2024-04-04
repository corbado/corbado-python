# coding: utf-8

"""
    Corbado Backend API

     # Introduction This documentation gives an overview of all Corbado Backend API calls to implement passwordless authentication with Passkeys.  The Corbado Backend API is organized around REST principles. It uses resource-oriented URLs with verbs (HTTP methods) and HTTP status codes. Requests need to be valid JSON payloads. We always return JSON.  The Corbado Backend API specification is written in **OpenAPI Version 3.0.3**. You can download it via the download button at the top and use it to generate clients in languages we do not provide officially for example.  # Authentication To authenticate your API requests HTTP Basic Auth is used.  You need to set the projectID as username and the API secret as password. The authorization header looks as follows:  `Basic <<projectID>:<API secret>>`  The **authorization header** needs to be **Base64 encoded** to be working. If the authorization header is missing or incorrect, the API will respond with status code 401.  # Error types As mentioned above we make use of HTTP status codes. **4xx** errors indicate so called client errors, meaning the error occurred on client side and you need to fix it. **5xx** errors indicate server errors, which means the error occurred on server side and outside your control.  Besides HTTP status codes Corbado uses what we call error types which gives more details in error cases and help you to debug your request.  ## internal_error The error type **internal_error** is used when some internal error occurred at Corbado. You can retry your request but usually there is nothing you can do about it. All internal errors get logged and will triggert an alert to our operations team which takes care of the situation as soon as possible.  ## not_found The error type **not_found** is used when you try to get a resource which cannot be found. Most common case is that you provided a wrong ID.  ## method_not_allowed The error type **method_not_allowed** is used when you use a HTTP method (GET for example) on a resource/endpoint which it not supports.   ## validation_error The error type **validation_error** is used when there is validation error on the data you provided in the request payload or path. There will be detailed information in the JSON response about the validation error like what exactly went wrong on what field.   ## project_id_mismatch The error type **project_id_mismatch** is used when there is a project ID you provided mismatch.  ## login_error The error type **login_error** is used when the authentication failed. Most common case is that you provided a wrong pair of project ID and API secret. As mentioned above with use HTTP Basic Auth for authentication.  ## invalid_json The error type **invalid_json** is used when you send invalid JSON as request body. There will be detailed information in the JSON response about what went wrong.  ## rate_limited The error type **rate_limited** is used when ran into rate limiting of the Corbado Backend API. Right now you can do a maximum of **2000 requests** within **10 seconds** from a **single IP**. Throttle your requests and try again. If you think you need more contact support@corbado.com.  ## invalid_origin The error type **invalid_origin** is used when the API has been called from a origin which is not authorized (CORS). Add the origin to your project at https://app.corbado.com/app/settings/credentials/authorized-origins.  ## already_exists The error type **already_exists** is used when you try create a resource which already exists. Most common case is that there is some unique constraint on one of the fields.  # Security and privacy Corbado services are designed, developed, monitored, and updated with security at our core to protect you and your customers’ data and privacy.  ## Security  ### Infrastructure security Corbado leverages highly available and secure cloud infrastructure to ensure that our services are always available and securely delivered. Corbado's services are operated in uvensys GmbH's data centers in Germany and comply with ISO standard 27001. All data centers have redundant power and internet connections to avoid failure. The main location of the servers used is in Linden and offers 24/7 support. We do not use any AWS, GCP or Azure services.  Each server is monitored 24/7 and in the event of problems, automated information is sent via SMS and e-mail. The monitoring is done by the external service provider Serverguard24 GmbH.   All Corbado hardware and networking is routinely updated and audited to ensure systems are secure and that least privileged access is followed. Additionally we implement robust logging and audit protocols that allow us high visibility into system use.  ### Responsible disclosure program Here at Corbado, we take the security of our user’s data and of our services seriously. As such, we encourage responsible security research on Corbado services and products. If you believe you’ve discovered a potential vulnerability, please let us know by emailing us at [security@corbado.com](mailto:security@corbado.com). We will acknowledge your email within 2 business days. As public disclosures of a security vulnerability could put the entire Corbado community at risk, we ask that you keep such potential vulnerabilities confidential until we are able to address them. We aim to resolve critical issues within 30 days of disclosure. Please make a good faith effort to avoid violating privacy, destroying data, or interrupting or degrading the Corbado service. Please only interact with accounts you own or for which you have explicit permission from the account holder. While researching, please refrain from:  - Distributed Denial of Service (DDoS) - Spamming - Social engineering or phishing of Corbado employees or contractors - Any attacks against Corbado's physical property or data centers  Thank you for helping to keep Corbado and our users safe!  ### Rate limiting At Corbado, we apply rate limit policies on our APIs in order to protect your application and user management infrastructure, so your users will have a frictionless non-interrupted experience.  Corbado responds with HTTP status code 429 (too many requests) when the rate limits exceed. Your code logic should be able to handle such cases by checking the status code on the response and recovering from such cases. If a retry is needed, it is best to allow for a back-off to avoid going into an infinite retry loop.  The current rate limit for all our API endpoints is **max. 100 requests per 10 seconds**.  ## Privacy Corbado is committed to protecting the personal data of our customers and their customers. Corbado has in place appropriate data security measures that meet industry standards. We regularly review and make enhancements to our processes, products, documentation, and contracts to help support ours and our customers’ compliance for the processing of personal data.  We try to minimize the usage and processing of personally identifiable information. Therefore, all our services are constructed to avoid unnecessary data consumption.  To make our services work, we only require the following data: - any kind of identifier (e.g. UUID, phone number, email address) - IP address (only temporarily for rate limiting aspects) - User agent (for device management) 

    The version of the OpenAPI document: 1.0.0
    Contact: support@corbado.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from corbado_python_sdk.generated.models.app_type import AppType
from corbado_python_sdk.generated.models.client_info import ClientInfo
from typing import Optional, Set
from typing_extensions import Self

class ProjectConfigSaveReq(BaseModel):
    """
    ProjectConfigSaveReq
    """ # noqa: E501
    external_name: Optional[StrictStr] = Field(default=None, alias="externalName")
    app_type: Optional[AppType] = Field(default=None, alias="appType")
    product_key: Optional[StrictStr] = Field(default=None, alias="productKey")
    email_from: Optional[StrictStr] = Field(default=None, alias="emailFrom")
    sms_from: Optional[StrictStr] = Field(default=None, alias="smsFrom")
    external_application_protocol_version: Optional[StrictStr] = Field(default=None, description="Defines which version of webhook is used", alias="externalApplicationProtocolVersion")
    webhook_url: Optional[StrictStr] = Field(default=None, alias="webhookURL")
    webhook_actions: Optional[List[StrictStr]] = Field(default=None, alias="webhookActions")
    webhook_username: Optional[StrictStr] = Field(default=None, alias="webhookUsername")
    webhook_password: Optional[StrictStr] = Field(default=None, alias="webhookPassword")
    webhook_test_invalid_username: Optional[StrictStr] = Field(default=None, alias="webhookTestInvalidUsername")
    webhook_test_valid_username: Optional[StrictStr] = Field(default=None, alias="webhookTestValidUsername")
    webhook_test_valid_password: Optional[StrictStr] = Field(default=None, alias="webhookTestValidPassword")
    external_application_username: Optional[StrictStr] = Field(default=None, alias="externalApplicationUsername")
    external_application_password: Optional[StrictStr] = Field(default=None, alias="externalApplicationPassword")
    legacy_auth_methods_url: Optional[StrictStr] = Field(default=None, alias="legacyAuthMethodsUrl")
    password_verify_url: Optional[StrictStr] = Field(default=None, alias="passwordVerifyUrl")
    auth_success_redirect_url: Optional[StrictStr] = Field(default=None, alias="authSuccessRedirectUrl")
    password_reset_url: Optional[StrictStr] = Field(default=None, alias="passwordResetUrl")
    allow_user_registration: Optional[StrictBool] = Field(default=None, alias="allowUserRegistration")
    allow_ip_stickiness: Optional[StrictBool] = Field(default=None, alias="allowIPStickiness")
    passkey_append_interval: Optional[StrictStr] = Field(default=None, alias="passkeyAppendInterval")
    fallback_language: Optional[StrictStr] = Field(default=None, alias="fallbackLanguage")
    auto_detect_language: Optional[StrictBool] = Field(default=None, alias="autoDetectLanguage")
    has_existing_users: Optional[StrictBool] = Field(default=None, alias="hasExistingUsers")
    has_verified_session: Optional[StrictBool] = Field(default=None, alias="hasVerifiedSession")
    has_generated_session: Optional[StrictBool] = Field(default=None, alias="hasGeneratedSession")
    has_started_using_passkeys: Optional[StrictBool] = Field(default=None, alias="hasStartedUsingPasskeys")
    has_started_using_sessions: Optional[StrictBool] = Field(default=None, alias="hasStartedUsingSessions")
    application_url: Optional[StrictStr] = Field(default=None, alias="applicationUrl")
    use_cli: Optional[StrictBool] = Field(default=None, alias="useCli")
    double_opt_in: Optional[StrictBool] = Field(default=None, alias="doubleOptIn")
    user_full_name_required: Optional[StrictBool] = Field(default=None, alias="userFullNameRequired")
    webauthn_rpid: Optional[StrictStr] = Field(default=None, alias="webauthnRPID")
    domain: Optional[StrictStr] = None
    cname: Optional[StrictStr] = None
    environment: Optional[StrictStr] = None
    frontend_framework: Optional[StrictStr] = Field(default=None, alias="frontendFramework")
    backend_language: Optional[StrictStr] = Field(default=None, alias="backendLanguage")
    web_component_debug: Optional[StrictBool] = Field(default=None, alias="webComponentDebug")
    smtp_use_custom: Optional[StrictBool] = Field(default=None, alias="smtpUseCustom")
    smtp_host: Optional[StrictStr] = Field(default=None, alias="smtpHost")
    smtp_port: Optional[StrictInt] = Field(default=None, alias="smtpPort")
    smtp_username: Optional[StrictStr] = Field(default=None, alias="smtpUsername")
    smtp_password: Optional[StrictStr] = Field(default=None, alias="smtpPassword")
    support_email: Optional[StrictStr] = Field(default=None, alias="supportEmail")
    signup_flow: Optional[StrictStr] = Field(default=None, alias="signupFlow")
    signup_flow_options: Optional[Dict[str, Any]] = Field(default=None, alias="signupFlowOptions")
    login_flow: Optional[StrictStr] = Field(default=None, alias="loginFlow")
    login_flow_options: Optional[Dict[str, Any]] = Field(default=None, alias="loginFlowOptions")
    request_id: Optional[StrictStr] = Field(default=None, description="Unique ID of request, you can provide your own while making the request, if not the ID will be randomly generated on server side", alias="requestID")
    client_info: Optional[ClientInfo] = Field(default=None, alias="clientInfo")
    __properties: ClassVar[List[str]] = ["externalName", "appType", "productKey", "emailFrom", "smsFrom", "externalApplicationProtocolVersion", "webhookURL", "webhookActions", "webhookUsername", "webhookPassword", "webhookTestInvalidUsername", "webhookTestValidUsername", "webhookTestValidPassword", "externalApplicationUsername", "externalApplicationPassword", "legacyAuthMethodsUrl", "passwordVerifyUrl", "authSuccessRedirectUrl", "passwordResetUrl", "allowUserRegistration", "allowIPStickiness", "passkeyAppendInterval", "fallbackLanguage", "autoDetectLanguage", "hasExistingUsers", "hasVerifiedSession", "hasGeneratedSession", "hasStartedUsingPasskeys", "hasStartedUsingSessions", "applicationUrl", "useCli", "doubleOptIn", "userFullNameRequired", "webauthnRPID", "domain", "cname", "environment", "frontendFramework", "backendLanguage", "webComponentDebug", "smtpUseCustom", "smtpHost", "smtpPort", "smtpUsername", "smtpPassword", "supportEmail", "signupFlow", "signupFlowOptions", "loginFlow", "loginFlowOptions", "requestID", "clientInfo"]

    @field_validator('external_application_protocol_version')
    def external_application_protocol_version_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['v1', 'v2']):
            raise ValueError("must be one of enum values ('v1', 'v2')")
        return value

    @field_validator('passkey_append_interval')
    def passkey_append_interval_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['0d', '1d', '3d', '1w', '3w', '1m', '3m']):
            raise ValueError("must be one of enum values ('0d', '1d', '3d', '1w', '3w', '1m', '3m')")
        return value

    @field_validator('environment')
    def environment_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['dev', 'prod']):
            raise ValueError("must be one of enum values ('dev', 'prod')")
        return value

    @field_validator('frontend_framework')
    def frontend_framework_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['react', 'vuejs', 'vanillajs', 'angular', 'svelte', 'nextjs', 'nuxtjs', 'flutter']):
            raise ValueError("must be one of enum values ('react', 'vuejs', 'vanillajs', 'angular', 'svelte', 'nextjs', 'nuxtjs', 'flutter')")
        return value

    @field_validator('backend_language')
    def backend_language_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['javascript', 'php', 'go', 'other']):
            raise ValueError("must be one of enum values ('javascript', 'php', 'go', 'other')")
        return value

    @field_validator('signup_flow')
    def signup_flow_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['PasskeyWithEmailOTPFallback', 'EmailOTPSignup']):
            raise ValueError("must be one of enum values ('PasskeyWithEmailOTPFallback', 'EmailOTPSignup')")
        return value

    @field_validator('login_flow')
    def login_flow_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['PasskeyWithEmailOTPFallback']):
            raise ValueError("must be one of enum values ('PasskeyWithEmailOTPFallback')")
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
        """Create an instance of ProjectConfigSaveReq from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of client_info
        if self.client_info:
            _dict['clientInfo'] = self.client_info.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProjectConfigSaveReq from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "externalName": obj.get("externalName"),
            "appType": obj.get("appType"),
            "productKey": obj.get("productKey"),
            "emailFrom": obj.get("emailFrom"),
            "smsFrom": obj.get("smsFrom"),
            "externalApplicationProtocolVersion": obj.get("externalApplicationProtocolVersion"),
            "webhookURL": obj.get("webhookURL"),
            "webhookActions": obj.get("webhookActions"),
            "webhookUsername": obj.get("webhookUsername"),
            "webhookPassword": obj.get("webhookPassword"),
            "webhookTestInvalidUsername": obj.get("webhookTestInvalidUsername"),
            "webhookTestValidUsername": obj.get("webhookTestValidUsername"),
            "webhookTestValidPassword": obj.get("webhookTestValidPassword"),
            "externalApplicationUsername": obj.get("externalApplicationUsername"),
            "externalApplicationPassword": obj.get("externalApplicationPassword"),
            "legacyAuthMethodsUrl": obj.get("legacyAuthMethodsUrl"),
            "passwordVerifyUrl": obj.get("passwordVerifyUrl"),
            "authSuccessRedirectUrl": obj.get("authSuccessRedirectUrl"),
            "passwordResetUrl": obj.get("passwordResetUrl"),
            "allowUserRegistration": obj.get("allowUserRegistration"),
            "allowIPStickiness": obj.get("allowIPStickiness"),
            "passkeyAppendInterval": obj.get("passkeyAppendInterval"),
            "fallbackLanguage": obj.get("fallbackLanguage"),
            "autoDetectLanguage": obj.get("autoDetectLanguage"),
            "hasExistingUsers": obj.get("hasExistingUsers"),
            "hasVerifiedSession": obj.get("hasVerifiedSession"),
            "hasGeneratedSession": obj.get("hasGeneratedSession"),
            "hasStartedUsingPasskeys": obj.get("hasStartedUsingPasskeys"),
            "hasStartedUsingSessions": obj.get("hasStartedUsingSessions"),
            "applicationUrl": obj.get("applicationUrl"),
            "useCli": obj.get("useCli"),
            "doubleOptIn": obj.get("doubleOptIn"),
            "userFullNameRequired": obj.get("userFullNameRequired"),
            "webauthnRPID": obj.get("webauthnRPID"),
            "domain": obj.get("domain"),
            "cname": obj.get("cname"),
            "environment": obj.get("environment"),
            "frontendFramework": obj.get("frontendFramework"),
            "backendLanguage": obj.get("backendLanguage"),
            "webComponentDebug": obj.get("webComponentDebug"),
            "smtpUseCustom": obj.get("smtpUseCustom"),
            "smtpHost": obj.get("smtpHost"),
            "smtpPort": obj.get("smtpPort"),
            "smtpUsername": obj.get("smtpUsername"),
            "smtpPassword": obj.get("smtpPassword"),
            "supportEmail": obj.get("supportEmail"),
            "signupFlow": obj.get("signupFlow"),
            "signupFlowOptions": obj.get("signupFlowOptions"),
            "loginFlow": obj.get("loginFlow"),
            "loginFlowOptions": obj.get("loginFlowOptions"),
            "requestID": obj.get("requestID"),
            "clientInfo": ClientInfo.from_dict(obj["clientInfo"]) if obj.get("clientInfo") is not None else None
        })
        return _obj


