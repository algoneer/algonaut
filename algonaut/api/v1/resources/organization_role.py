from algonaut.models import Organization
from algonaut.api.resource import Resource, ResponseType
from algonaut.api.decorators import authorized
from flask import request


class OrganizationRoles(Resource):
    @authorized()
    def get(self) -> ResponseType:
        return {"data": [org_roles.export() for org_roles in request.user.roles]}, 200
