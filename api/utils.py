from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled):
        response_data = {
            'detail': 'request limit exceeded',
            'availableAfter': str(exc.wait // 60) + " min"
        }
        response.data = response_data
        response.status_code = status.HTTP_429_TOO_MANY_REQUESTS

    return response
