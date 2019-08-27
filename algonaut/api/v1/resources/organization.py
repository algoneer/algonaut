from algonaut.models import Organization
from algonaut.api.resource import Resource, ResponseType
from algonaut.api.decorators import authorized
from flask import request


class Organizations(Resource):
    @authorized()
    def get(self) -> ResponseType:
        organizations = []
        for org_roles in request.user.roles:
            organization = org_roles.organization.export()
            organization["roles"] = org_roles.export(with_org=False)["roles"]
            organizations.append(organization)
        return {"data": organizations}, 200
