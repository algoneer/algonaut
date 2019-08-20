from flask import request
from functools import wraps
from algonaut.settings import settings
from algonaut.api.resource import ResponseType

from typing import Iterable, Optional, Callable


def authorized(
    scopes=None, superuser=False, roles: Optional[Iterable[str]] = None
) -> Callable[[Callable[..., ResponseType]], Callable[..., ResponseType]]:

    """
    Ensures that the request originates from a valid user.
    """

    unauthorized: ResponseType = ({"message": "unauthorized"}, 403)

    def decorator(f) -> Callable[..., ResponseType]:
        @wraps(f)
        def decorated_function(*args, **kwargs) -> ResponseType:
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

    return decorator
