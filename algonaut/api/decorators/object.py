from flask import request
from functools import wraps
from algonaut.settings import settings
from algonaut.models import Base, ObjectRole

from typing import Type, Iterable, Optional, Any


def valid_object(
    Type: Type[Base], roles: Optional[Iterable[str]] = None, id_field: str = "object_id"
):

    """
    Ensure that a user has access rights for the given object
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            object_id = kwargs.get(id_field)
            if not object_id:
                return {"message": "invalid ID"}, 400

            def authorize(session) -> Any:

                obj = (
                    session.query(Type)
                    .filter(Type.ext_id == object_id, Type.deleted_at == None)
                    .one_or_none()
                )
                if not obj:
                    return {"message": "not found"}, 404

                obj_roles = ObjectRole.roles_for(session, request.user, obj)
                obj_roles_strs = set([role.object_role for role in obj_roles])
                if roles is None:
                    if not obj_roles:
                        return {"message": "not found"}, 404
                else:
                    for role in roles:
                        if role in obj_roles_strs:
                            break
                    else:
                        return {"message": "not found"}, 404
                obj._roles = obj_roles
                setattr(request, obj.type(), obj)
                return f(*args, **kwargs)

            if hasattr(request, "session"):
                return authorize(request.session)
            with settings.session() as session:
                request.session = session
                return authorize(session)

        return decorated_function

    return decorator
