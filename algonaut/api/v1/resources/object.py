from ...resource import Resource
from algonaut.models import ObjectRole, Base
from algonaut.settings import settings
from algonaut.utils.forms import Form
from flask import request
from ...decorators import authorized, valid_object

from typing import Type, Optional


def Objects(
    Type: Type[Base], Form: Type[Form], Dependent: Optional[Type[Base]] = None
) -> Type[Resource]:
    class Objects(Resource):
        @authorized
        def get(self):
            """
            Return all objects that match the given criteria and that the user is
            allowed to see.
            """
            with settings.session() as session:
                visible_objs = ObjectRole.select_for(session, request.user, Type.type())
                objs = (
                    session.query(Type)
                    .filter(Type.ext_id.in_(visible_objs), Type.deleted_at == None)
                    .all()
                )
                return {"data": [obj.export() for obj in objs]}, 200

        @authorized(roles=["admin"])
        def post(self):
            form = Form(self.t, request.get_json() or {})
            if not form.validate():
                return {"message": "invalid data", "errors": form.errors}, 400
            with settings.session() as session:
                obj = Type(**form.data)
                session.add(obj)
                session.commit()
                # we create an object role for the newly created object
                ObjectRole.get_or_create(
                    session, obj, request.user.roles.organization, "admin", "admin"
                )
                return obj.export(), 201

    return Objects


def ObjectDetails(
    Type: Type[Base], Form: Type[Form], Dependent: Optional[Type[Base]] = None
) -> Type[Resource]:
    class ObjectDetails(Resource):
        @authorized
        @valid_object(Type, roles=["admin", "view"])
        def get(self, object_id):
            return getattr(request, Type.type()).export(), 200

        @authorized
        @valid_object(Type, roles=["admin"])
        def patch(self, object_id):
            form = Form(self.t, request.get_json() or {}, is_update=True)
            if not form.validate():
                return {"message": "invalid data", "errors": form.errors}, 400
            for name, value in form.data.items():
                obj = getattr(request, Type.type())
                setattr(obj, name, value)
            request.session.commit()
            return obj.export(), 200

        @authorized(roles=["admin"])
        @valid_object(Type, roles=["admin"])
        def delete(self, object_id):
            obj = getattr(request, Type.type())
            obj.delete(request.session)
            request.session.commit()
            return {"message": "success"}, 200

    return ObjectDetails
