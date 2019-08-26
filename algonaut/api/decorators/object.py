from flask import request
from functools import wraps
from algonaut.settings import settings
from algonaut.api.resource import ResponseType
from algonaut.models import Base, ObjectRole
from sqlalchemy.orm import joinedload
import sqlalchemy

from typing import Type, Iterable, Optional, Any, List, Callable


def valid_object(
    Type: Optional[Type[Base]],
    roles: Optional[Iterable[str]] = None,
    id_field: str = "object_id",
    dependent_id_field: str = "dependent_id",
    DependentTypes: Optional[List[Type[Base]]] = None,
    Joins: Optional[List[List[Type[Base]]]] = None,
    JoinBy: Optional[Type[Base]] = None,
) -> Callable[[Callable[..., ResponseType]], Callable[..., ResponseType]]:

    """
    Ensure that a user has access rights for the given object
    """

    not_found = {"message": "not found"}, 404

    def decorator(f: Callable[..., ResponseType]) -> Callable[..., ResponseType]:
        @wraps(f)
        def decorated_function(*args, **kwargs) -> ResponseType:

            if Type is None:
                # if not type is given, we return the original result without change
                return f(*args, **kwargs)

            object_id = kwargs.get(id_field)
            if not object_id:
                return {"message": "invalid ID"}, 400

            def authorize(session: sqlalchemy.orm.session.Session) -> ResponseType:

                # required to make mypy happy
                assert Type is not None

                # we retrieve the requested object from the database
                query = session.query(Type).filter(
                    Type.ext_id == object_id, Type.deleted_at == None
                )

                if Joins:
                    for j in Joins:
                        joinedloads = None
                        for Join in j:
                            if joinedloads is None:
                                joinedloads = joinedload(Join, innerjoin=True)
                            else:
                                joinedloads = joinedloads.joinedload(
                                    Join, innerjoin=True
                                )
                        query = query.options(joinedloads)

                obj = query.one_or_none()

                if not obj:
                    return not_found

                if Type is ObjectRole:
                    # this is an object role, we check if the user has admin
                    # privileges for the organization.
                    if not "admin" in request.user.roles.roles:
                        return not_found
                else:
                    if DependentTypes:
                        # this object depends on a chain of dependent objects from which it
                        # inherits roles. We therefore need to retrieve these dependent objects
                        # from the database.
                        DependentType = DependentTypes[0]
                        dependent_id = kwargs.get(dependent_id_field)
                        if dependent_id:
                            # if a dependent ID is given in the URL, we retrieve
                            # the dependent object through this
                            query = session.query(DependentType).filter(
                                DependentType.ext_id == dependent_id,
                                DependentType.deleted_at == None,
                            )
                        else:
                            # otherwise, we retrieve the object by its relation
                            # to the main object.
                            if JoinBy is not None:
                                # if there is a M2M table that we should join by, we
                                # include it in the query to ensure there is an actual entry between
                                # the requested object and the dependent objects
                                query = (
                                    session.query(DependentType)
                                    .filter(DependentType.deleted_at == None)
                                    .join(JoinBy)
                                    .filter(
                                        getattr(JoinBy, obj.type) == obj,
                                        getattr(
                                            JoinBy, "{}_id".format(DependentType().type)
                                        )
                                        == DependentType.id,
                                        DependentType.deleted_at == None,
                                    )
                                )
                            else:
                                query = session.query(DependentType).filter(
                                    DependentType.id
                                    == getattr(
                                        obj, "{}_id".format(DependentType().type)
                                    ),
                                    DependentType.deleted_at == None,
                                )
                        if len(DependentTypes) > 1:
                            # if there are more than one dependent types, we add joinedload
                            # conditions for all of them to make sure they get loaded efficiently
                            # from the database.
                            joinedloads = None
                            for NextType in DependentTypes[1:]:
                                nt = NextType().type
                                query = query.filter(NextType.deleted_at == None)
                                if joinedloads is None:
                                    joinedloads = joinedload(
                                        getattr(DependentType, nt), innerjoin=True
                                    )
                                else:
                                    joinedloads = joinedloads.joinedload(
                                        getattr(DependentType, nt), innerjoin=True
                                    )
                                DependentType = NextType
                                # if the dependent type has an organization
                                # we also load it...
                                if hasattr(DependentType, "organization"):
                                    joinedloads = joinedloads.joinedload(
                                        DependentType.organization, innerjoin=True
                                    )
                            query = query.options(joinedloads)

                        dependent_obj = query.one_or_none()

                        if not dependent_obj:
                            return not_found

                        # we extract the dependent types from the object and store them
                        # on the request object
                        setattr(request, dependent_obj.type, dependent_obj)
                        for DependentType in DependentTypes[1:]:
                            next_type = DependentType().type
                            next_obj = getattr(dependent_obj, next_type)
                            if next_obj is None:
                                return not_found
                            setattr(request, next_type, next_obj)
                            dependent_obj = next_obj
                        # we set the role object to the last object in the dependency chain
                        role_obj = dependent_obj
                    else:
                        role_obj = obj

                    role_found = False
                    # this object is owned by an organization, so we check the roles of
                    # the currently logged in user in the organization and see if the
                    # the user is an admin or superuser, in which case he/she has access
                    # to the object regardless of explicitly set object roles.
                    if (
                        hasattr(role_obj, "organization")
                        and not role_obj.organization.deleted_at
                    ):
                        for org_roles in request.user.roles:
                            if (
                                org_roles.organization.id
                                == role_obj.organization.source_id
                                and org_roles.organization.source
                                == role_obj.organization.source
                            ):
                                for role in ["admin", "superuser"]:
                                    if role in org_roles.roles:
                                        role_found = True
                                        break
                                else:
                                    continue
                                break
                    # we retrieve the roles for the role object and the currently logged in user
                    obj_roles = ObjectRole.roles_for(session, request.user, role_obj)
                    obj_roles_set = set([role.object_role for role in obj_roles])
                    # we check the roles against the required ones to see if the user has one of the
                    # requested roles on the object, otherwise we return "not found"
                    if roles is None:
                        if obj_roles:
                            role_found = True
                    else:
                        for role in roles:
                            if role in obj_roles_set:
                                role_found = True
                                break
                    if not role_found:
                        return not_found
                    # we add the roles to the object as a context information
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
