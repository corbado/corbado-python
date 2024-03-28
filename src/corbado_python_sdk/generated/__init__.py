# coding: utf-8

# flake8: noqa

"""
    Corbado Backend API

     # Introduction This documentation gives an overview of all Corbado Backend API calls to implement passwordless authentication with Passkeys.  The Corbado Backend API is organized around REST principles. It uses resource-oriented URLs with verbs (HTTP methods) and HTTP status codes. Requests need to be valid JSON payloads. We always return JSON.  The Corbado Backend API specification is written in **OpenAPI Version 3.0.3**. You can download it via the download button at the top and use it to generate clients in languages we do not provide officially for example.  # Authentication To authenticate your API requests HTTP Basic Auth is used.  You need to set the projectID as username and the API secret as password. The authorization header looks as follows:  `Basic <<projectID>:<API secret>>`  The **authorization header** needs to be **Base64 encoded** to be working. If the authorization header is missing or incorrect, the API will respond with status code 401.  # Error types As mentioned above we make use of HTTP status codes. **4xx** errors indicate so called client errors, meaning the error occurred on client side and you need to fix it. **5xx** errors indicate server errors, which means the error occurred on server side and outside your control.  Besides HTTP status codes Corbado uses what we call error types which gives more details in error cases and help you to debug your request.  ## internal_error The error type **internal_error** is used when some internal error occurred at Corbado. You can retry your request but usually there is nothing you can do about it. All internal errors get logged and will triggert an alert to our operations team which takes care of the situation as soon as possible.  ## not_found The error type **not_found** is used when you try to get a resource which cannot be found. Most common case is that you provided a wrong ID.  ## method_not_allowed The error type **method_not_allowed** is used when you use a HTTP method (GET for example) on a resource/endpoint which it not supports.   ## validation_error The error type **validation_error** is used when there is validation error on the data you provided in the request payload or path. There will be detailed information in the JSON response about the validation error like what exactly went wrong on what field.   ## project_id_mismatch The error type **project_id_mismatch** is used when there is a project ID you provided mismatch.  ## login_error The error type **login_error** is used when the authentication failed. Most common case is that you provided a wrong pair of project ID and API secret. As mentioned above with use HTTP Basic Auth for authentication.  ## invalid_json The error type **invalid_json** is used when you send invalid JSON as request body. There will be detailed information in the JSON response about what went wrong.  ## rate_limited The error type **rate_limited** is used when ran into rate limiting of the Corbado Backend API. Right now you can do a maximum of **2000 requests** within **10 seconds** from a **single IP**. Throttle your requests and try again. If you think you need more contact support@corbado.com.  ## invalid_origin The error type **invalid_origin** is used when the API has been called from a origin which is not authorized (CORS). Add the origin to your project at https://app.corbado.com/app/settings/credentials/authorized-origins.  ## already_exists The error type **already_exists** is used when you try create a resource which already exists. Most common case is that there is some unique constraint on one of the fields.  # Security and privacy Corbado services are designed, developed, monitored, and updated with security at our core to protect you and your customers’ data and privacy.  ## Security  ### Infrastructure security Corbado leverages highly available and secure cloud infrastructure to ensure that our services are always available and securely delivered. Corbado's services are operated in uvensys GmbH's data centers in Germany and comply with ISO standard 27001. All data centers have redundant power and internet connections to avoid failure. The main location of the servers used is in Linden and offers 24/7 support. We do not use any AWS, GCP or Azure services.  Each server is monitored 24/7 and in the event of problems, automated information is sent via SMS and e-mail. The monitoring is done by the external service provider Serverguard24 GmbH.   All Corbado hardware and networking is routinely updated and audited to ensure systems are secure and that least privileged access is followed. Additionally we implement robust logging and audit protocols that allow us high visibility into system use.  ### Responsible disclosure program Here at Corbado, we take the security of our user’s data and of our services seriously. As such, we encourage responsible security research on Corbado services and products. If you believe you’ve discovered a potential vulnerability, please let us know by emailing us at [security@corbado.com](mailto:security@corbado.com). We will acknowledge your email within 2 business days. As public disclosures of a security vulnerability could put the entire Corbado community at risk, we ask that you keep such potential vulnerabilities confidential until we are able to address them. We aim to resolve critical issues within 30 days of disclosure. Please make a good faith effort to avoid violating privacy, destroying data, or interrupting or degrading the Corbado service. Please only interact with accounts you own or for which you have explicit permission from the account holder. While researching, please refrain from:  - Distributed Denial of Service (DDoS) - Spamming - Social engineering or phishing of Corbado employees or contractors - Any attacks against Corbado's physical property or data centers  Thank you for helping to keep Corbado and our users safe!  ### Rate limiting At Corbado, we apply rate limit policies on our APIs in order to protect your application and user management infrastructure, so your users will have a frictionless non-interrupted experience.  Corbado responds with HTTP status code 429 (too many requests) when the rate limits exceed. Your code logic should be able to handle such cases by checking the status code on the response and recovering from such cases. If a retry is needed, it is best to allow for a back-off to avoid going into an infinite retry loop.  The current rate limit for all our API endpoints is **max. 100 requests per 10 seconds**.  ## Privacy Corbado is committed to protecting the personal data of our customers and their customers. Corbado has in place appropriate data security measures that meet industry standards. We regularly review and make enhancements to our processes, products, documentation, and contracts to help support ours and our customers’ compliance for the processing of personal data.  We try to minimize the usage and processing of personally identifiable information. Therefore, all our services are constructed to avoid unnecessary data consumption.  To make our services work, we only require the following data: - any kind of identifier (e.g. UUID, phone number, email address) - IP address (only temporarily for rate limiting aspects) - User agent (for device management) 

    The version of the OpenAPI document: 1.0.0
    Contact: support@corbado.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


__version__ = "1.0.0"

# import apis into sdk package
from generated.api.api_secrets_api import APISecretsApi
from generated.api.analyzer_api import AnalyzerApi
from generated.api.android_app_config_api import AndroidAppConfigApi
from generated.api.association_tokens_api import AssociationTokensApi
from generated.api.auth_methods_api import AuthMethodsApi
from generated.api.auth_tokens_api import AuthTokensApi
from generated.api.email_otp_api import EmailOTPApi
from generated.api.email_magic_links_api import EmailMagicLinksApi
from generated.api.email_templates_api import EmailTemplatesApi
from generated.api.examples_api import ExamplesApi
from generated.api.long_sessions_api import LongSessionsApi
from generated.api.passkeys_biometrics_api import PasskeysBiometricsApi
from generated.api.project_config_api import ProjectConfigApi
from generated.api.request_logs_api import RequestLogsApi
from generated.api.smsotp_api import SMSOTPApi
from generated.api.sms_templates_api import SMSTemplatesApi
from generated.api.session_config_api import SessionConfigApi
from generated.api.user_api import UserApi
from generated.api.validation_api import ValidationApi
from generated.api.webhook_logs_api import WebhookLogsApi
from generated.api.ios_app_config_api import IOSAppConfigApi

# import ApiClient
from generated.api_response import ApiResponse
from generated.api_client import ApiClient
from generated.configuration import Configuration
from generated.exceptions import OpenApiException
from generated.exceptions import ApiTypeError
from generated.exceptions import ApiValueError
from generated.exceptions import ApiKeyError
from generated.exceptions import ApiAttributeError
from generated.exceptions import ApiException

# import models into sdk package
from generated.models.android_app_config_delete_req import AndroidAppConfigDeleteReq
from generated.models.android_app_config_item import AndroidAppConfigItem
from generated.models.android_app_config_list_rsp import AndroidAppConfigListRsp
from generated.models.android_app_config_save_req import AndroidAppConfigSaveReq
from generated.models.android_app_config_save_rsp import AndroidAppConfigSaveRsp
from generated.models.android_app_config_update_req import AndroidAppConfigUpdateReq
from generated.models.android_app_config_update_rsp import AndroidAppConfigUpdateRsp
from generated.models.app_type import AppType
from generated.models.association_token_create_req import AssociationTokenCreateReq
from generated.models.association_token_create_rsp import AssociationTokenCreateRsp
from generated.models.association_token_create_rsp_all_of_data import AssociationTokenCreateRspAllOfData
from generated.models.auth_method import AuthMethod
from generated.models.auth_methods_list_req import AuthMethodsListReq
from generated.models.auth_methods_list_rsp import AuthMethodsListRsp
from generated.models.auth_methods_list_rsp_all_of_data import AuthMethodsListRspAllOfData
from generated.models.auth_token_validate_req import AuthTokenValidateReq
from generated.models.auth_token_validate_rsp import AuthTokenValidateRsp
from generated.models.client_info import ClientInfo
from generated.models.custom_login_identifier import CustomLoginIdentifier
from generated.models.email import Email
from generated.models.email_code import EmailCode
from generated.models.email_code_get_rsp import EmailCodeGetRsp
from generated.models.email_code_get_rsp_all_of_data import EmailCodeGetRspAllOfData
from generated.models.email_code_send_req import EmailCodeSendReq
from generated.models.email_code_send_rsp import EmailCodeSendRsp
from generated.models.email_code_send_rsp_all_of_data import EmailCodeSendRspAllOfData
from generated.models.email_code_validate_req import EmailCodeValidateReq
from generated.models.email_code_validate_rsp import EmailCodeValidateRsp
from generated.models.email_link import EmailLink
from generated.models.email_link_get_rsp import EmailLinkGetRsp
from generated.models.email_link_get_rsp_all_of_data import EmailLinkGetRspAllOfData
from generated.models.email_link_send_req import EmailLinkSendReq
from generated.models.email_link_send_rsp import EmailLinkSendRsp
from generated.models.email_link_send_rsp_all_of_data import EmailLinkSendRspAllOfData
from generated.models.email_link_validate_rsp import EmailLinkValidateRsp
from generated.models.email_links_delete_req import EmailLinksDeleteReq
from generated.models.email_links_validate_req import EmailLinksValidateReq
from generated.models.email_template_create_req import EmailTemplateCreateReq
from generated.models.email_template_create_rsp import EmailTemplateCreateRsp
from generated.models.email_template_create_rsp_all_of_data import EmailTemplateCreateRspAllOfData
from generated.models.email_template_delete_req import EmailTemplateDeleteReq
from generated.models.email_validation_result import EmailValidationResult
from generated.models.empty_req import EmptyReq
from generated.models.error_rsp import ErrorRsp
from generated.models.error_rsp_all_of_error import ErrorRspAllOfError
from generated.models.error_rsp_all_of_error_validation import ErrorRspAllOfErrorValidation
from generated.models.example_get_rsp import ExampleGetRsp
from generated.models.full_user import FullUser
from generated.models.generic_rsp import GenericRsp
from generated.models.ios_app_config_delete_req import IOSAppConfigDeleteReq
from generated.models.ios_app_config_item import IOSAppConfigItem
from generated.models.ios_app_config_list_rsp import IOSAppConfigListRsp
from generated.models.ios_app_config_save_req import IOSAppConfigSaveReq
from generated.models.ios_app_config_save_rsp import IOSAppConfigSaveRsp
from generated.models.ios_app_config_update_req import IOSAppConfigUpdateReq
from generated.models.ios_app_config_update_rsp import IOSAppConfigUpdateRsp
from generated.models.login_identifier_type import LoginIdentifierType
from generated.models.long_session import LongSession
from generated.models.long_session_get_rsp import LongSessionGetRsp
from generated.models.long_session_get_rsp_all_of_data import LongSessionGetRspAllOfData
from generated.models.long_session_list_rsp import LongSessionListRsp
from generated.models.long_session_list_rsp_all_of_data import LongSessionListRspAllOfData
from generated.models.long_session_revoke_req import LongSessionRevokeReq
from generated.models.paging import Paging
from generated.models.phone_number import PhoneNumber
from generated.models.phone_number_validation_result import PhoneNumberValidationResult
from generated.models.project_config import ProjectConfig
from generated.models.project_config_get_rsp import ProjectConfigGetRsp
from generated.models.project_config_save_req import ProjectConfigSaveReq
from generated.models.project_config_webhook_test_req import ProjectConfigWebhookTestReq
from generated.models.project_config_webhook_test_rsp import ProjectConfigWebhookTestRsp
from generated.models.project_config_webhook_test_rsp_all_of_data import ProjectConfigWebhookTestRspAllOfData
from generated.models.project_secret_create_req import ProjectSecretCreateReq
from generated.models.project_secret_create_rsp import ProjectSecretCreateRsp
from generated.models.project_secret_delete_req import ProjectSecretDeleteReq
from generated.models.project_secret_item import ProjectSecretItem
from generated.models.project_secret_list_rsp import ProjectSecretListRsp
from generated.models.request_data import RequestData
from generated.models.request_log import RequestLog
from generated.models.request_log_get_rsp import RequestLogGetRsp
from generated.models.request_logs_list_rsp import RequestLogsListRsp
from generated.models.request_logs_list_rsp_all_of_data import RequestLogsListRspAllOfData
from generated.models.session_config import SessionConfig
from generated.models.session_config_get_rsp import SessionConfigGetRsp
from generated.models.session_config_update_req import SessionConfigUpdateReq
from generated.models.session_token_create_req import SessionTokenCreateReq
from generated.models.session_token_create_rsp import SessionTokenCreateRsp
from generated.models.session_token_create_rsp_all_of_data import SessionTokenCreateRspAllOfData
from generated.models.session_token_verify_req import SessionTokenVerifyReq
from generated.models.session_token_verify_rsp import SessionTokenVerifyRsp
from generated.models.session_token_verify_rsp_all_of_data import SessionTokenVerifyRspAllOfData
from generated.models.sms_code_send_req import SmsCodeSendReq
from generated.models.sms_code_send_rsp import SmsCodeSendRsp
from generated.models.sms_code_send_rsp_all_of_data import SmsCodeSendRspAllOfData
from generated.models.sms_code_validate_req import SmsCodeValidateReq
from generated.models.sms_code_validate_rsp import SmsCodeValidateRsp
from generated.models.sms_template_create_req import SmsTemplateCreateReq
from generated.models.sms_template_create_rsp import SmsTemplateCreateRsp
from generated.models.sms_template_create_rsp_all_of_data import SmsTemplateCreateRspAllOfData
from generated.models.sms_template_delete_req import SmsTemplateDeleteReq
from generated.models.status import Status
from generated.models.tracking_backup_state import TrackingBackupState
from generated.models.tracking_backup_state_get_rsp import TrackingBackupStateGetRsp
from generated.models.tracking_browser_detailed_stats import TrackingBrowserDetailedStats
from generated.models.tracking_browser_detailed_stats_list_rsp import TrackingBrowserDetailedStatsListRsp
from generated.models.tracking_browser_detailed_stats_list_rsp_all_of_data import TrackingBrowserDetailedStatsListRspAllOfData
from generated.models.tracking_browser_stats import TrackingBrowserStats
from generated.models.tracking_browser_stats_list_rsp import TrackingBrowserStatsListRsp
from generated.models.tracking_browser_stats_list_rsp_all_of_data import TrackingBrowserStatsListRspAllOfData
from generated.models.tracking_detailed_stats import TrackingDetailedStats
from generated.models.tracking_detailed_stats_list_rsp import TrackingDetailedStatsListRsp
from generated.models.tracking_detailed_stats_list_rsp_all_of_data import TrackingDetailedStatsListRspAllOfData
from generated.models.tracking_enums import TrackingEnums
from generated.models.tracking_enums_get_rsp import TrackingEnumsGetRsp
from generated.models.tracking_os_detailed_stats import TrackingOSDetailedStats
from generated.models.tracking_os_detailed_stats_list_rsp import TrackingOSDetailedStatsListRsp
from generated.models.tracking_os_detailed_stats_list_rsp_all_of_data import TrackingOSDetailedStatsListRspAllOfData
from generated.models.tracking_os_stats import TrackingOSStats
from generated.models.tracking_os_stats_list_rsp import TrackingOSStatsListRsp
from generated.models.tracking_os_stats_list_rsp_all_of_data import TrackingOSStatsListRspAllOfData
from generated.models.tracking_raw_list_row import TrackingRawListRow
from generated.models.tracking_raw_list_rsp import TrackingRawListRsp
from generated.models.tracking_stats import TrackingStats
from generated.models.tracking_stats_list_rsp import TrackingStatsListRsp
from generated.models.tracking_stats_list_rsp_all_of_data import TrackingStatsListRspAllOfData
from generated.models.user import User
from generated.models.user_auth_log import UserAuthLog
from generated.models.user_auth_log_list_rsp import UserAuthLogListRsp
from generated.models.user_auth_log_list_rsp_all_of_data import UserAuthLogListRspAllOfData
from generated.models.user_create_req import UserCreateReq
from generated.models.user_create_rsp import UserCreateRsp
from generated.models.user_create_rsp_all_of_data import UserCreateRspAllOfData
from generated.models.user_custom_login_identifier_create_req import UserCustomLoginIdentifierCreateReq
from generated.models.user_custom_login_identifier_create_rsp import UserCustomLoginIdentifierCreateRsp
from generated.models.user_custom_login_identifier_create_rsp_all_of_data import UserCustomLoginIdentifierCreateRspAllOfData
from generated.models.user_custom_login_identifier_delete_req import UserCustomLoginIdentifierDeleteReq
from generated.models.user_custom_login_identifier_get_rsp import UserCustomLoginIdentifierGetRsp
from generated.models.user_custom_login_identifier_get_rsp_all_of_data import UserCustomLoginIdentifierGetRspAllOfData
from generated.models.user_delete_req import UserDeleteReq
from generated.models.user_device import UserDevice
from generated.models.user_device_list_rsp import UserDeviceListRsp
from generated.models.user_email import UserEmail
from generated.models.user_email_create_req import UserEmailCreateReq
from generated.models.user_email_create_rsp import UserEmailCreateRsp
from generated.models.user_email_create_rsp_all_of_data import UserEmailCreateRspAllOfData
from generated.models.user_email_delete_req import UserEmailDeleteReq
from generated.models.user_email_get_rsp import UserEmailGetRsp
from generated.models.user_email_get_rsp_all_of_data import UserEmailGetRspAllOfData
from generated.models.user_exists_req import UserExistsReq
from generated.models.user_exists_rsp import UserExistsRsp
from generated.models.user_get_rsp import UserGetRsp
from generated.models.user_list_rsp import UserListRsp
from generated.models.user_list_rsp_all_of_data import UserListRspAllOfData
from generated.models.user_phone_number import UserPhoneNumber
from generated.models.user_phone_number_create_req import UserPhoneNumberCreateReq
from generated.models.user_phone_number_create_rsp import UserPhoneNumberCreateRsp
from generated.models.user_phone_number_create_rsp_all_of_data import UserPhoneNumberCreateRspAllOfData
from generated.models.user_phone_number_delete_req import UserPhoneNumberDeleteReq
from generated.models.user_phone_number_get_rsp import UserPhoneNumberGetRsp
from generated.models.user_phone_number_get_rsp_all_of_data import UserPhoneNumberGetRspAllOfData
from generated.models.user_stats import UserStats
from generated.models.user_stats_list_rsp import UserStatsListRsp
from generated.models.user_stats_list_rsp_all_of_data import UserStatsListRspAllOfData
from generated.models.user_update_req import UserUpdateReq
from generated.models.user_update_rsp import UserUpdateRsp
from generated.models.user_username import UserUsername
from generated.models.validate_email_req import ValidateEmailReq
from generated.models.validate_email_rsp import ValidateEmailRsp
from generated.models.validate_phone_number_req import ValidatePhoneNumberReq
from generated.models.validate_phone_number_rsp import ValidatePhoneNumberRsp
from generated.models.validation_email import ValidationEmail
from generated.models.validation_phone_number import ValidationPhoneNumber
from generated.models.web_authn_associate_start_req import WebAuthnAssociateStartReq
from generated.models.web_authn_associate_start_rsp import WebAuthnAssociateStartRsp
from generated.models.web_authn_authenticate_finish_rsp import WebAuthnAuthenticateFinishRsp
from generated.models.web_authn_authenticate_start_req import WebAuthnAuthenticateStartReq
from generated.models.web_authn_authenticate_start_rsp import WebAuthnAuthenticateStartRsp
from generated.models.web_authn_authenticate_success import WebAuthnAuthenticateSuccess
from generated.models.web_authn_authenticator_update_req import WebAuthnAuthenticatorUpdateReq
from generated.models.web_authn_credential_exists_req import WebAuthnCredentialExistsReq
from generated.models.web_authn_credential_exists_rsp import WebAuthnCredentialExistsRsp
from generated.models.web_authn_credential_item_rsp import WebAuthnCredentialItemRsp
from generated.models.web_authn_credential_list_rsp import WebAuthnCredentialListRsp
from generated.models.web_authn_credential_req import WebAuthnCredentialReq
from generated.models.web_authn_credential_rsp import WebAuthnCredentialRsp
from generated.models.web_authn_finish_req import WebAuthnFinishReq
from generated.models.web_authn_mediation_start_req import WebAuthnMediationStartReq
from generated.models.web_authn_mediation_start_rsp import WebAuthnMediationStartRsp
from generated.models.web_authn_register_finish_rsp import WebAuthnRegisterFinishRsp
from generated.models.web_authn_register_start_req import WebAuthnRegisterStartReq
from generated.models.web_authn_register_start_rsp import WebAuthnRegisterStartRsp
from generated.models.webauthn_setting_create import WebauthnSettingCreate
from generated.models.webauthn_setting_create_req import WebauthnSettingCreateReq
from generated.models.webauthn_setting_create_rsp import WebauthnSettingCreateRsp
from generated.models.webauthn_setting_delete_req import WebauthnSettingDeleteReq
from generated.models.webauthn_setting_get_rsp import WebauthnSettingGetRsp
from generated.models.webauthn_setting_item import WebauthnSettingItem
from generated.models.webauthn_setting_list_rsp import WebauthnSettingListRsp
from generated.models.webauthn_setting_update_req import WebauthnSettingUpdateReq
from generated.models.webauthn_setting_update_rsp import WebauthnSettingUpdateRsp
from generated.models.webhook_log import WebhookLog
from generated.models.webhook_logs_list_rsp import WebhookLogsListRsp
from generated.models.webhook_logs_list_rsp_all_of_data import WebhookLogsListRspAllOfData
