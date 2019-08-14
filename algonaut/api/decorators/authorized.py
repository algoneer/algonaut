from flask import request
from functools import wraps
from algonaut.settings import settings


def authorized(f=None, scopes=None, superuser=False):

    """
    Ensures that the request originates from a valid user.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client = settings.auth_client
            # the client retrieves the user object for the given request
            user = client.get_user(request)
            if user is None:
                return {"message": "unauthorized"}, 403
            request.user = user
            return f(*args, **kwargs)

        return decorated_function

    if f:
        return decorator(f)
    else:
        return decorator
