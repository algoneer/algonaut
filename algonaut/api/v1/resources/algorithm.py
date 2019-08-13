from ...resource import Resource
from algonaut.models import ObjectRole
from algonaut.settings import settings
from flask import request
from ...decorators import authorized


class Algorithms(Resource):
    @authorized
    def get(self):
        """
        Return all objects that match the given criteria and that the user is
        allowed to see.
        """
        with settings.session() as session:
            visible_objs = ObjectRole.select_for(session, request.user, "algorithm", [])
            return {}, 200
