from ...resource import Resource, ResponseType
from algonaut.models import ObjectRole, Base, Organization, Hashable
from algonaut.settings import settings
from algonaut.utils.forms import Form
from algonaut.utils.auth import User
from flask import request
from ...decorators import authorized, valid_object

import datetime
import sqlalchemy
from sqlalchemy.sql import and_, or_
from sqlalchemy.orm import joinedload
from typing import Type, Optional, List, Dict, Any


def admin_orgs_id_query(session: sqlalchemy.orm.session.Session, user: User):
    """
    Returns all organizations in which the user is either admin or superuser.
    Used to retrieve objects for which the user doesn't have a specific role
    but which he/she can nevertheless see as an admin/superuser.
    """
    filters = []
    for org_roles in user.roles:
        if "admin" in org_roles.roles or "superuser" in org_roles.roles:
            filters.extend(
                [
                    and_(
                        Organization.source_id == org_roles.organization.id,
                        Organization.source == org_roles.organization.source,
                        Organization.deleted_at == None,
                    )
                ]
            )
    return session.query(Organization.id).filter(or_(*filters))


def Objects(
    Type: Type[Base],
    Form: Type[Form],
    DependentTypes: Optional[List[Type[Base]]] = None,
    JoinBy: Optional[Type[Base]] = None,
    Joins: Optional[List[List[Type[Base]]]] = None,
) -> Type[Resource]:
    """
    Returns a resource that retrieves a list of objects and creates new objects.
    
    :param           Type: The model for which to list or create objects.
    :param           Form: The form to use for validating data when creating objects.
    :param DependentTypes: Models that this model depends on for access rights.
    :param         JoinBy: A M2M model to use for joining the given model to the dependent
                           models, in case the relationship is not one-to-many.
    :param          Joins: An optional list of lists of models to join to the result set.
                           Useful to load dependent object in a single database query.
    :             returns: A resource that can be used for listing and creating objects of the
                           given type.
    """

    class Objects(Resource):
        @authorized()
        @valid_object(
            DependentTypes[0] if DependentTypes else None,
            roles=["view", "admin"],
            DependentTypes=DependentTypes[1:] if DependentTypes else None,
        )
        def get(self, object_id: Optional[str] = None) -> ResponseType:
            """
            Return all objects that match the given criteria and that the user is
            allowed to see.
            """
            with settings.session() as session:
                if DependentTypes:
                    dependent_type = DependentTypes[0]().type
                    dependent_obj = getattr(request, dependent_type)
                    filters = [Type.deleted_at == None]
                    joins = []
                    if JoinBy:
                        joins.append(JoinBy)
                        filters.extend(
                            [getattr(JoinBy, dependent_type) == dependent_obj]
                        )
                    else:
                        filters.append(getattr(Type, dependent_type) == dependent_obj)
                    query = session.query(Type).filter(*filters).join(*joins)
                else:
                    visible_objs = ObjectRole.select_for(
                        session, request.user, Type().type
                    )
                    # we add objects visible via the users organizations
                    org_ids = admin_orgs_id_query(session, request.user)
                    query = session.query(Type).filter(
                        or_(
                            Type.id.in_(visible_objs), Type.organization_id.in_(org_ids)
                        ),
                        Type.deleted_at == None,
                    )

                # If requested, we join dependent objects for faster response times...
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
                objs = query.all()

                return {"data": [obj.export() for obj in objs]}, 200

        @authorized(
            roles=["admin", "superuser", "creator"] if not DependentTypes else None
        )
        @valid_object(
            DependentTypes[0] if DependentTypes else None,
            roles=["admin"],
            DependentTypes=DependentTypes[1:] if DependentTypes else None,
        )
        def post(
            self, object_id: Optional[str] = None, organization_id: Optional[str] = None
        ) -> ResponseType:
            form = Form(request.get_json() or {})
            if not form.validate():
                return {"message": "invalid data", "errors": form.errors}, 400

            dependent_obj: Optional[Base] = None
            org: Optional[Organization] = None
            join_by: Optional[Base] = None

            if DependentTypes:
                dependent_type = DependentTypes[0]().type
                dependent_obj = getattr(request, dependent_type)

            with settings.session() as session:

                obj = Type(**form.valid_data)

                if organization_id is not None:
                    org = Organization.get_or_create(session, request.organization)
                    obj.organization = org

                if dependent_obj:
                    if JoinBy:
                        # if this object has a M2M table, we create a row in
                        # the table for the newly created object
                        join_by = JoinBy()
                        setattr(join_by, dependent_type, dependent_obj)
                        setattr(join_by, obj.type, obj)
                    else:
                        setattr(obj, dependent_type, dependent_obj)

                # we expunge the object from the session, as it might have been added
                # when we associated the dependent properties with it...
                session.expunge(obj)

                existing_obj = obj.get_existing(session)

                if existing_obj:
                    return existing_obj.export(), 201

                if isinstance(obj, Hashable):
                    extra_args = []
                    if dependent_obj and not JoinBy:
                        extra_args = [getattr(Type, dependent_type) == dependent_obj]
                    existing_obj = (
                        session.query(Type)
                        .filter(
                            Type.hash == obj.hash, Type.deleted_at == None, *extra_args
                        )
                        .one_or_none()
                    )
                    if existing_obj:
                        return existing_obj.export(), 201

                if join_by:
                    session.add(join_by)

                session.add(obj)

                if not DependentTypes:
                    # we create an object role for the newly created object
                    # only if it does not depends on another object
                    assert isinstance(org, Organization)
                    for org_role in ["admin", "superuser"]:
                        ObjectRole.get_or_create(session, obj, org, "admin", org_role)

                session.commit()

                return obj.export(), 201

    return Objects


def ObjectDetails(
    Type: Type[Base],
    Form: Type[Form],
    DependentTypes: Optional[List[Type[Base]]] = None,
    JoinBy: Optional[Type[Base]] = None,
    Joins: Optional[List[List[Type[Base]]]] = None,
) -> Type[Resource]:
    """
    Returns a resource that gets, updates and deletes objects of a given type.
    
    :param           Type: The model for which to get, update or delete objects.
    :param           Form: The form to use for validating data when updating objects.
    :param DependentTypes: Models that this model depends on for access rights.
    :param          Joins: An optional list of lists of models to join to the result set.
                           Useful to load dependent object in a single database query.
    :             returns: A resource that can be used for getting, updating and deleting
                           objects of the given type.
    """

    class ObjectDetails(Resource):
        @authorized()
        @valid_object(
            Type,
            roles=["admin", "view"],
            DependentTypes=DependentTypes,
            JoinBy=JoinBy,
            Joins=Joins,
        )
        def get(
            self, object_id: str, dependent_id: Optional[str] = None
        ) -> ResponseType:
            return getattr(request, Type().type).export(), 200

        @authorized()
        @valid_object(
            Type, roles=["admin"], DependentTypes=DependentTypes, JoinBy=JoinBy
        )
        def patch(
            self, object_id: str, dependent_id: Optional[str] = None
        ) -> ResponseType:
            form = Form(request.get_json() or {}, is_update=True)
            if not form.validate():
                return {"message": "invalid data", "errors": form.errors}, 400
            obj = getattr(request, Type().type)
            for name, value in form.valid_data.items():
                setattr(obj, name, value)
            request.session.commit()
            return obj.export(), 200

        @authorized()
        @valid_object(
            Type, roles=["admin"], DependentTypes=DependentTypes, JoinBy=JoinBy
        )
        def delete(
            self, object_id: str, dependent_id: Optional[str] = None
        ) -> ResponseType:
            obj = getattr(request, Type().type)
            obj.deleted_at = datetime.datetime.utcnow()
            request.session.commit()
            return {"message": "success"}, 200

    return ObjectDetails
