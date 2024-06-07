<img width="1070" alt="GitHub Repo Cover" src="https://github.com/corbado/corbado-php/assets/18458907/aa4f9df6-980b-4b24-bb2f-d71c0f480971">

# Corbado Python SDK

[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![documentation](https://img.shields.io/badge/documentation-Corbado_Backend_API_Reference-blue.svg)](https://api.corbado.com/docs/api/)
[![Slack](https://img.shields.io/badge/slack-join%20chat-brightgreen.svg)](https://join.slack.com/t/corbado/shared_invite/zt-1b7867yz8-V~Xr~ngmSGbt7IA~g16ZsQ)

The [Corbado](https://www.corbado.com) Python SDK provides convenient access to the [Corbado Backend API](https://api.corbado.com/docs/api/) from applications written in the Python language.

:warning: The Corbado Python SDK is commonly referred to as a private client, specifically designed for usage within closed backend applications. This particular SDK should exclusively be utilized in such environments, as it is crucial to ensure that the API secret remains strictly confidential and is never shared.

:rocket: [Getting started](#rocket-getting-started) | :hammer_and_wrench: [Services](#hammer_and_wrench-services) | :books: [Advanced](#books-advanced) | :speech_balloon: [Support & Feedback](#speech_balloon-support--feedback)

## :rocket: Getting started

### Requirements

- Python 3.8 or later

### Installation

Use the following command to install the Corbado Python SDK:

```bash
pip install passkeys (Warning: Package is not yet published)
```

### Usage

To create a Corbado Python SDK instance you need to provide your `Project ID` and `API secret` which can be found at the [Developer Panel](https://app.corbado.com).

```Python
config: Config = Config(project_id="{project_id}", api_secret="c{api_secret}")
sdk = CorbadoSDK(config=config)
```

### Examples

A list of examples can be found in the integration tests [here](tests/integration).

## :hammer_and_wrench: Services

The Corbado Python SDK provides the following services:

- `auth_tokens` for managing authentication tokens needed for own session management ([examples](tests/integration/test_auth_token_service.py))
- `email_magic_links` for managing email magic links ([examples](tests/integration/test_email_magic_link_service.py))
- `email_otps` for managing email OTPs ([examples](tests/integration/test_email_otp_service.py))
- `sessions` for managing sessions ([example flask app](tests/utils/session_service_example.py))
- `sms_otps` for managing SMS OTPs ([examples](tests/integration/test_sms_otp_service.py))
- `users` for managing users ([examples](tests/integration/test_user_service.py))
- `validations` for validating email addresses and phone numbers ([examples](tests/integration/test_validation_service.py))

To use a specific service, such as `users`, invoke it as shown below:

```Python
user_service: UserInterface = sdk.users
``` 

## :books: Advanced

### Error handling

The Corbado Python SDK throws exceptions for all errors. The following exceptions are thrown:

- `ValidationError` for failed validations (client side)
- `ServerException` for server errors (server side)
- `StandardException` for everything else (client side)

If the Backend API returns a HTTP status code other than 200, the Corbado Python SDK throws a `ServerException`. The `ServerException`class provides convenient methods to access all important data:
  sdk.users.get(user_id="usr-123456789")

```Python
        try:
            # Try to get non-existing user with ID 'usr-123456789'
            sdk.users.get(user_id="usr-123456789")
        except ServerException as e:
            # Show HTTP status code (404 in this case)
            print(f"Status Code: {e.http_status_code}")

            # Show request ID (can be used in developer panel to look up the full request
            # and response, see https://app.corbado.com/app/logs/requests)
            print(f"Request id: {e.request_id}")

            # Show full request data
            print(f"Request data: {e.request_data}")

            # Show runtime of request in seconds (server side)
            print(f"Runtime: {e.runtime}")

            # Show error type (not_found)
            print(f"Error type: {e.error_type}")

            # Show full error data
            print(f"Full error: {e.error}")

```
## Developer Setup

Create a virtual environment and install packages -
``` console
python3 -m venv venv_name
source venv_name/bin/activate
pip install -r requirements-dev.txt
```
(Add venv_name to "exclude" list in .flake8, otherwise flake8 will lint the generated venv)

Add environment variables for tests (use the test project from secrets repositoty) -
``` console
export CORBADO_API_SECRET=corbado1_123456
export CORBADO_PROJECT_ID=pro-123456
export CORBADO_BACKEND_API=https://backendapi.corbado.io
```

# Testing

Run all tests using -

``` console
tox run -e py38
```

The tox tests are configured to run on Python  3.8, 3.9, 3.10, 3.11, 3.12 (you need to remove "-e py38" tox argument)

Run linting and mypy:
``` console
mypy -p corbado_python_sdk --exclude generated --strict --disable-error-code attr-defined
flake8 .
```

# Development notes

Use Version file as single source of truth for version control.

Use VSCode with provided project/extentions configuration .vscode/settings.json

Use the recommended extentions from .vscode/extentions.json and explore their functionality to achieve expected code quality by integration tests:



## :speech_balloon: Support & Feedback

### Report an issue

If you encounter any bugs or have suggestions, please [open an issue](https://github.com/corbado/corbado-python/issues/new).

### Slack channel

Join our Slack channel to discuss questions or ideas with the Corbado team and other developers.

[![Slack](https://img.shields.io/badge/slack-join%20chat-brightgreen.svg)](https://join.slack.com/t/corbado/shared_invite/zt-1b7867yz8-V~Xr~ngmSGbt7IA~g16ZsQ)

### Email

You can also reach out to us via email at vincent.delitz@corbado.com.

### Vulnerability reporting

Please report suspected security vulnerabilities in private to security@corbado.com. Please do NOT create publicly viewable issues for suspected security vulnerabilities.
