from ...resource import Resource, ResponseType
from algonaut.models import ObjectRole, Base
from algonaut.settings import settings
from algonaut.utils.forms import Form
from flask import request
from ...decorators import authorized, valid_object

from typing import Type, Optional, List


def Objects(
    Type: Type[Base],
    Form: Type[Form],
    DependentTypes: Optional[List[Type[Base]]] = None,
    JoinBy: Optional[Type[Base]] = None,
) -> Type[Resource]:
    """
    Returns a resource that retrieves a list of objects and creates new objects.
    
    :param           Type: The model for which to list or create objects.
    :param           Form: The form to use for validating data when creating objects.
    :param DependentTypes: Models that this model depends on for access rights.
    :param         JoinBy: A M2M model to use for joining the given model to the dependent
                           models, in case the relationship is not one-to-many.
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
                    objs = session.query(Type).filter(*filters).join(*joins).all()
                else:
                    visible_objs = ObjectRole.select_for(
                        session, request.user, Type().type
                    )
                    objs = (
                        session.query(Type)
                        .filter(Type.ext_id.in_(visible_objs), Type.deleted_at == None)
                        .all()
                    )
                return {"data": [obj.export() for obj in objs]}, 200

        @authorized(roles=["admin"])
        @valid_object(
            DependentTypes[0] if DependentTypes else None,
            roles=["view", "admin"],
            DependentTypes=DependentTypes[1:] if DependentTypes else None,
        )
        def post(self, object_id: Optional[str] = None) -> ResponseType:
            form = Form(self.t, request.get_json() or {})
            if not form.validate():
                return {"message": "invalid data", "errors": form.errors}, 400
            with settings.session() as session:
                obj = Type(**form.valid_data)
                if DependentTypes:
                    dependent_type = DependentTypes[0]().type
                    dependent_obj = getattr(request, dependent_type)
                    if JoinBy:
                        # if this object has a M2M table, we create a row in
                        # the table for the newly created object
                        join_by = JoinBy()
                        setattr(join_by, dependent_type, dependent_obj)
                        setattr(join_by, obj.type, obj)
                        session.add(join_by)
                    else:
                        setattr(obj, dependent_type, dependent_obj)
                session.add(obj)
                session.commit()
                if not DependentTypes:
                    # we create an object role for the newly created object
                    # only if it does not depends on another object
                    ObjectRole.get_or_create(
                        session, obj, request.user.roles.organization, "admin", "admin"
                    )
                return obj.export(), 201

    return Objects


def ObjectDetails(
    Type: Type[Base],
    Form: Type[Form],
    DependentTypes: Optional[List[Type[Base]]] = None,
    JoinBy: Optional[Type[Base]] = None,
) -> Type[Resource]:
    """
    Returns a resource that gets, updates and deletes objects of a given type.
    
    :param           Type: The model for which to get, update or delete objects.
    :param           Form: The form to use for validating data when updating objects.
    :param DependentTypes: Models that this model depends on for access rights.
    :             returns: A resource that can be used for getting, updating and deleting
                           objects of the given type.
    """

    class ObjectDetails(Resource):
        @authorized()
        @valid_object(
            Type, roles=["admin", "view"], DependentTypes=DependentTypes, JoinBy=JoinBy
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
            form = Form(self.t, request.get_json() or {}, is_update=True)
            if not form.validate():
                return {"message": "invalid data", "errors": form.errors}, 400
            obj = getattr(request, Type().type)
            for name, value in form.valid_data.items():
                setattr(obj, name, value)
            request.session.commit()
            return obj.export(), 200

        @authorized(roles=["admin"])
        @valid_object(
            Type, roles=["admin"], DependentTypes=DependentTypes, JoinBy=JoinBy
        )
        def delete(
            self, object_id: str, dependent_id: Optional[str] = None
        ) -> ResponseType:
            obj = getattr(request, Type().type)
            obj.delete(request.session)
            request.session.commit()
            return {"message": "success"}, 200

    return ObjectDetails
