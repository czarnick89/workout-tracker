from rest_framework.views import exception_handler
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_response = {
            "error": {
                "code": response.status_code,
                "message": None,
            }
        }

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            error_response["error"]["code"] = "validation_error"
            # Put detailed field errors directly inside "message"
            error_response["error"]["message"] = response.data

        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            error_response["error"]["code"] = "authentication_failed"
            error_response["error"]["message"] = "Authentication credentials were not provided or are invalid."

        elif response.status_code == status.HTTP_403_FORBIDDEN:
            error_response["error"]["code"] = "permission_denied"
            error_response["error"]["message"] = "You do not have permission to perform this action."

        else:
            if isinstance(response.data, dict) and "detail" in response.data:
                error_response["error"]["message"] = response.data["detail"]
            else:
                error_response["error"]["message"] = response.data

        response.data = error_response

    return response
