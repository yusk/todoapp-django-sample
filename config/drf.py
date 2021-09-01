from rest_framework.views import exception_handler
from django.core.exceptions import ValidationError
from rest_framework.serializers import ValidationError as DRFValidationError


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        exc = DRFValidationError(exc.message_dict)
    return exception_handler(exc, context)
