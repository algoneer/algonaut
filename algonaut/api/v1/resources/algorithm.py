from ...resource import Resource
from algonaut.models import ObjectRole, Algorithm
from algonaut.settings import settings
from flask import request
from ...decorators import authorized, valid_object
from ..forms import AlgorithmForm


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

    @authorized(roles=["admin"])
    def post(self):
        form = AlgorithmForm(self.t, request.get_json() or {})
        if not form.validate():
            return {"message": "invalid data", "errors": form.errors}, 400
        with settings.session() as session:
            algorithm = Algorithm(**form.data)
            session.add(algorithm)
            session.commit()
            return algorithm.export(), 201


class AlgorithmDetails(Resource):
    @authorized
    @valid_object(Algorithm, roles=["admin", "view"])
    def get(self, object_id):
        return request.algorithm.export(), 200

    @authorized
    @valid_object(Algorithm, roles=["admin"])
    def patch(self, object_id):
        form = AlgorithmForm(self.t, request.get_json() or {}, is_update=True)
        if not form.validate():
            return {"message": "invalid data", "errors": form.errors}, 400
        for name, value in form.data.items():
            setattr(request.algorithm, name, value)
        request.session.commit()
        return request.algorithm.export(), 200

    @authorized(roles=["admin"])
    @valid_object(Algorithm, roles=["admin"])
    def delete(self, object_id):
        request.algorithm.delete(request.session)
        request.session.commit()
        return {"message": "success"}, 200
