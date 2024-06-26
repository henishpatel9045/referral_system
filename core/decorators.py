from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return Response(
                {"message": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": e.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

    return wrapper
