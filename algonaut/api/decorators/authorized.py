import re
from flask import request
from functools import wraps
from algonaut.settings import settings
from algonaut.api.resource import ResponseType
from algonaut.utils.auth import User

from typing import Iterable, Optional, Callable


def authorized(
    scopes=None,
    superuser=False,
    roles: Optional[Iterable[str]] = None,
    org_id_field: str = "organization_id",
) -> Callable[[Callable[..., ResponseType]], Callable[..., ResponseType]]:

    """
    Ensures that the request originates from a valid user.
    """

    unauthorized: ResponseType = ({"message": "unauthorized"}, 403)

    def decorator(f) -> Callable[..., ResponseType]:
        @wraps(f)
        def decorated_function(*args, **kwargs) -> ResponseType:
            def get_org_roles(user: User):
                org_id = kwargs.get(org_id_field)
                if not isinstance(org_id, str):
                    return
                if not re.match(r"^[a-f0-9]+$", org_id):
                    return
                binary_org_id = bytearray.fromhex(org_id)
                for org_roles in user.roles:
                    if org_roles.organization.id == binary_org_id:
                        break
                else:
                    return
                if roles:
                    for role in roles:
                        if role in org_roles.roles:
                            break
                    else:
                        return
                return org_roles

            client = settings.auth_client
            # the client retrieves the user object for the given request
            user = client.get_user(request)
            if user is None:
                return unauthorized
            if roles:
                # if roles are defined, we assume that an organization_id was
                # speficied as well, so we try to find it and validate that
                # the user has the corresponding role
                org_roles = get_org_roles(user)
                if not org_roles:
                    return unauthorized
                request.org_roles = org_roles
                request.organization = org_roles.organization

            request.user = user
            return f(*args, **kwargs)

        return decorated_function

    return decorator
