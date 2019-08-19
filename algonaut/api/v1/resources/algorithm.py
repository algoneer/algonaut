from ...resource import Resource
from algonaut.models import ObjectRole, Algorithm
from algonaut.settings import settings
from flask import request
from ...decorators import authorized, valid_object


class Algorithms(Resource):
    @authorized
    def get(self):
        """
        Return all objects that match the given criteria and that the user is
        allowed to see.
        """
        with settings.session() as session:
            visible_algos = ObjectRole.select_for(session, request.user, "algorithm")
            algorithms = (
                session.query(Algorithm)
                .filter(
                    Algorithm.ext_id.in_(visible_algos), Algorithm.deleted_at == None
                )
                .all()
            )
            return {"data": [algorithm.export() for algorithm in algorithms]}, 200


class AlgorithmDetails(Resource):
    @authorized
    @valid_object(Algorithm, roles=["admin", "view"])
    def get(self, object_id):
        return request.algorithm.export(), 200
