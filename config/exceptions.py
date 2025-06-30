import logging
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Handle Django model DoesNotExist exceptions
    if isinstance(exc, ObjectDoesNotExist):
        return Response({
            "error": {
                "code": "not_found",
                "message": "The requested resource was not found."
            }
        }, status=status.HTTP_404_NOT_FOUND)

    # Let DRF handle the exception first
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
            error_response["error"]["message"] = response.data

        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            error_response["error"]["code"] = "authentication_failed"
            error_response["error"]["message"] = (
                "Authentication credentials were not provided or are invalid."
            )

        elif response.status_code == status.HTTP_403_FORBIDDEN:
            error_response["error"]["code"] = "permission_denied"
            error_response["error"]["message"] = (
                "You do not have permission to perform this action."
            )

        elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            error_response["error"]["code"] = "server_error"
            error_response["error"]["message"] = (
                "An unexpected error occurred. Please try again later."
            )
            logger.error(f"500 Internal Server Error: {exc} | Context: {context}")

        else:
            detail = getattr(exc, "detail", None)
            if detail:
                error_response["error"]["message"] = str(detail)
            else:
                error_response["error"]["message"] = response.data
            logger.warning(f"Unhandled exception: {exc} | Context: {context}")

        response.data = error_response

    return response
