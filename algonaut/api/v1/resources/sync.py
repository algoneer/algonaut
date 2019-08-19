from ...resource import Resource
from algonaut.models import ObjectRole, Algorithm
from algonaut.settings import settings
from flask import request
from ...decorators import authorized


class Sync(Resource):

    """
    The sync endpoint allows the Python library to send one large request with
    algorithms, algorithm versions, models, datasets, datapoints and results
    to the API. The API will reply with a
    """

    @authorized
    def post(self):
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
