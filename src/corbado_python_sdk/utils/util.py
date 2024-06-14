import json
from typing import Any, Dict, List

from corbado_python_sdk.exceptions.standard_exception import StandardException
from corbado_python_sdk.generated import GenericRsp, RequestData


class Util:
    """Helper class containing various utility methods."""

    @staticmethod
    def json_encode(data: Any) -> str:
        """JSON encode.

        Args:
            data (Any): Data to be encoded.

        Raises:
            StandardException: If encoding fails.

        Returns:
            str: Encoded JSON string.
        """
        try:
            json_str: str = json.dumps(data)
        except TypeError as e:
            raise StandardException(f"json.dumps() failed: {e}")
        except OverflowError as e:
            raise StandardException(f"json.dumps() failed: {e}")
        except ValueError as e:
            raise StandardException(f"json.dumps() failed: {e}")
        except RecursionError as e:
            raise StandardException(f"json.dumps() failed: {e}")
        except Exception as e:
            raise StandardException(f"json.dumps() failed: {e}")
        return json_str

    @staticmethod
    def json_decode(data: str) -> Dict[str, Any]:
        """
        JSON decode.

        Args:
            data (str): Data to be decoded.

        Raises:
            StandardException: If decoding fails.

        Returns:
            Dict[str, Any]: Decoded data as a dictionary.
        """
        try:
            decoded_data: Dict[str, Any] = json.loads(data)
        except json.JSONDecodeError as e:
            raise StandardException(f"json.loads() failed: {e}")
        except TypeError as e:
            raise StandardException(f"json.loads() failed: {e}")
        except Exception as e:
            raise StandardException(f"json.loads() failed: {e}")

        return decoded_data

    @staticmethod
    def is_error_http_status_code(status_code: int) -> bool:
        """
        Check if the status code indicates an error.

        Args:
            status_code (int): Status code.

        Returns:
            bool: True if status code indicates an error, False otherwise.
        """
        return status_code >= 300

    @staticmethod
    def hydrate_request_data(data: Dict[str, Any]) -> RequestData:
        """
        Hydrate RequestData object from dictionary.

        Args:
            data (Dict[str, Any]): Data.

        Raises:
            StandardException: If required keys are missing in the data.

        Returns:
            RequestData: RequestData object.
        """
        keys_to_check: List[str] = ["requestID", "link"]
        for key in keys_to_check:
            if key not in data:
                raise StandardException(f"Key '{key}' not found in data")
        return RequestData(requestID=data["requestID"], link=data["link"])

    @staticmethod
    def hydrate_response(data: Dict[str, Any]) -> GenericRsp:
        """
        Hydrate GenericRsp object from dictionary.

        Args:
            data (Dict[str, Any]): Data.

        Raises:
            StandardException: If required keys are missing in the data.

        Returns:
            GenericRsp: GenericRsp object.
        """
        keys_to_check: List[str] = ["httpStatusCode", "message", "requestData", "runtime"]
        for key in keys_to_check:
            if key not in data:
                raise StandardException(f"Key '{key}' not found in data")
        request_data: RequestData = Util.hydrate_request_data(data["requestData"])
        return GenericRsp(
            httpStatusCode=data["httpStatusCode"],
            message=data["message"],
            requestData=request_data,
            runtime=data["runtime"],
        )
