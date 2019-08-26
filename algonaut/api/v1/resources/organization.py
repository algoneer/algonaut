from algonaut.models import Organization
from algonaut.api.resource import Resource, ResponseType
from algonaut.api.decorators import authorized
from flask import request


class Organizations(Resource):
    @authorized()
    def get(self) -> ResponseType:
        return {}, 200
