from flask import request
from functools import wraps
from algonaut.settings import settings
from algonaut.models import Base, ObjectRole

from typing import Type, Iterable, Optional, Any


def valid_object(
    Type: Optional[Type[Base]],
    roles: Optional[Iterable[str]] = None,
    id_field: str = "object_id",
    dependent_id_field: str = "dependent_id",
    DependentType: Optional[Type[Base]] = None,
):

    """
    Ensure that a user has access rights for the given object
    """

    not_found = {"message": "not found"}, 404

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if Type is None:
                return f(*args, **kwargs)

            object_id = kwargs.get(id_field)
            if not object_id:
                return {"message": "invalid ID"}, 400

            def authorize(session) -> Any:

                # required to make mypy happy
                assert Type is not None

                obj = (
                    session.query(Type)
                    .filter(Type.ext_id == object_id, Type.deleted_at == None)
                    .one_or_none()
                )
                if not obj:
                    return not_found

                if Type is ObjectRole:
                    # this is an object role, we check if the user has admin
                    # privileges for the organization.
                    if not "admin" in request.user.roles.roles:
                        return not_found
                else:
                    if DependentType is not None:
                        # this object "inherits" roles from a dependent object
                        dependent_id = kwargs.get(dependent_id_field)
                        dependent_obj = (
                            session.query(DependentType)
                            .filter(
                                DependentType.ext_id == dependent_id,
                                DependentType.deleted_at == None,
                            )
                            .one_or_none()
                        )
                        if not dependent_obj:
                            return not_found
                        setattr(request, dependent_obj.type, dependent_obj)
                        role_obj = dependent_obj
                    else:
                        role_obj = obj
                    obj_roles = ObjectRole.roles_for(session, request.user, role_obj)
                    obj_roles_set = set([role.object_role for role in obj_roles])
                    if roles is None:
                        if not obj_roles:
                            return not_found
                    else:
                        for role in roles:
                            if role in obj_roles_set:
                                break
                        else:
                            return not_found
                    obj._roles = obj_roles
                setattr(request, obj.type, obj)
                return f(*args, **kwargs)

            if hasattr(request, "session"):
                return authorize(request.session)
            with settings.session() as session:
                request.session = session
                return authorize(session)

        return decorated_function

    return decorator
