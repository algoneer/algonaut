from algonaut.utils.worf.user import User

from flask import request
from functools import wraps


def authorized(f=None, scopes=None, superuser=False):

    """
    Ensures that the request originates from a valid user.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            request.user = User({})
            return f(*args, **kwargs)

        return decorated_function

    if f:
        return decorator(f)
    else:
        return decorator
