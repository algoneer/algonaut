from flask import request
from functools import wraps
from algonaut.settings import settings

from typing import Iterable, Optional


def authorized(
    f=None, scopes=None, superuser=False, roles: Optional[Iterable[str]] = None
):

    """
    Ensures that the request originates from a valid user.
    """

    unauthorized = {"message": "unauthorized"}, 403

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client = settings.auth_client
            # the client retrieves the user object for the given request
            user = client.get_user(request)
            if user is None:
                return unauthorized
            if roles:
                for role in roles:
                    if role in user.roles.roles:
                        break
                else:
                    return unauthorized

            request.user = user
            return f(*args, **kwargs)

        return decorated_function

    if f:
        return decorator(f)
    else:
        return decorator
