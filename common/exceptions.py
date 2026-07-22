from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Global API exception handler.
    """
    response = exception_handler(exc, context)
    if response is not None:
        custom_response = {
            "success": False,
            "message": "Request failed.",
            "errors": response.data,
        }
        response.data = custom_response
    return response
