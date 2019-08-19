from ...resource import Resource
from algonaut.models import ObjectRole, Base
from algonaut.settings import settings
from algonaut.utils.forms import Form
from flask import request
from ...decorators import authorized, valid_object

from typing import Type, Optional


def Objects(
    Type: Type[Base], Form: Type[Form], DependentType: Optional[Type[Base]] = None
) -> Type[Resource]:
    class Objects(Resource):
        @authorized
        @valid_object(DependentType, roles=["view", "admin"])
        def get(self, object_id=None):
            """
            Return all objects that match the given criteria and that the user is
            allowed to see.
            """
            with settings.session() as session:
                if DependentType is not None:
                    dependent_type = DependentType().type
                    dependent_obj = getattr(request, dependent_type)
                    filters = [
                        getattr(Type, dependent_type) == dependent_obj,
                        Type.deleted_at == None,
                    ]
                    objs = session.query(Type).filter(*filters).all()
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
        @valid_object(DependentType, roles=["view", "admin"])
        def post(self, object_id=None):
            form = Form(self.t, request.get_json() or {})
            if not form.validate():
                return {"message": "invalid data", "errors": form.errors}, 400
            with settings.session() as session:
                obj = Type(**form.data)
                if DependentType is not None:
                    dependent_type = DependentType().type
                    dependent_obj = getattr(request, dependent_type)
                    setattr(obj, dependent_type, dependent_obj)
                session.add(obj)
                session.commit()
                # we create an object role for the newly created object
                ObjectRole.get_or_create(
                    session, obj, request.user.roles.organization, "admin", "admin"
                )
                return obj.export(), 201

    return Objects


def ObjectDetails(
    Type: Type[Base], Form: Type[Form], DependentType: Optional[Type[Base]] = None
) -> Type[Resource]:
    class ObjectDetails(Resource):
        @authorized
        @valid_object(Type, roles=["admin", "view"], DependentType=DependentType)
        def get(self, object_id, dependent_id=None):
            return getattr(request, Type().type).export(), 200

        @authorized
        @valid_object(Type, roles=["admin"], DependentType=DependentType)
        def patch(self, object_id, dependent_id=None):
            form = Form(self.t, request.get_json() or {}, is_update=True)
            if not form.validate():
                return {"message": "invalid data", "errors": form.errors}, 400
            obj = getattr(request, Type().type)
            for name, value in form.data.items():
                setattr(obj, name, value)
            request.session.commit()
            return obj.export(), 200

        @authorized(roles=["admin"])
        @valid_object(Type, roles=["admin"], DependentType=DependentType)
        def delete(self, object_id, dependent_id=None):
            obj = getattr(request, Type().type)
            obj.delete(request.session)
            request.session.commit()
            return {"message": "success"}, 200

    return ObjectDetails
