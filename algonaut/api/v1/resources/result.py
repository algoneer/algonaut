from algonaut.models import (
    Result,
    Model,
    ModelResult,
    Datapoint,
    DatasetVersionDatapoint,
    DatapointModelResult,
    AlgorithmVersionResult,
    DatasetVersionResult,
    AlgorithmVersion,
    DatasetVersion,
    Dataset,
    Algorithm,
)
from ..forms import ResultForm
from .object import Objects, ObjectDetails

from algonaut.api.resource import Resource, ResponseType
from algonaut.api.decorators import valid_object, authorized
from algonaut.settings import settings
from flask import request

from typing import Optional

# Returns results for a given dataset version
DatasetVersionResults = Objects(
    Result, ResultForm, [DatasetVersion, Dataset], DatasetVersionResult
)
DatasetVersionResultDetails = ObjectDetails(
    Result, ResultForm, [DatasetVersion, Dataset], DatasetVersionResult
)

# Returns results for a given algorithm version
AlgorithmVersionResults = Objects(
    Result, ResultForm, [AlgorithmVersion, Algorithm], AlgorithmVersionResult
)
AlgorithmVersionResultDetails = ObjectDetails(
    Result, ResultForm, [AlgorithmVersion, Algorithm], AlgorithmVersionResult
)

# Returns results for a given model version
ModelResults = Objects(
    Result, ResultForm, [Model, AlgorithmVersion, Algorithm], ModelResult
)
ModelResultDetails = ObjectDetails(
    Result, ResultForm, [Model, AlgorithmVersion, Algorithm], ModelResult
)

DatapointModelResultDetails = ObjectDetails(
    Result, ResultForm, [Model, AlgorithmVersion, Algorithm], DatapointModelResult
)


class DatapointModelResults(Resource):
    @authorized(roles=["admin"])
    @valid_object(
        Datapoint,
        roles=["view", "admin"],
        DependentTypes=[DatasetVersion, Dataset],
        JoinBy=DatasetVersionDatapoint,
        id_field="datapoint_id",
    )
    @valid_object(
        Model,
        roles=["view", "admin"],
        DependentTypes=[AlgorithmVersion, Algorithm],
        id_field="model_id",
    )
    def get(self, datapoint_id: str, model_id: str) -> ResponseType:
        """
        Return all objects that match the given criteria and that the user is
        allowed to see.
        """
        with settings.session() as session:
            filters = [
                Result.deleted_at == None,
                DatapointModelResult.datapoint == request.datapoint,
                DatapointModelResult.model == request.model,
            ]
            objs = (
                session.query(Result).filter(*filters).join(DatapointModelResult).all()
            )
            return {"data": [obj.export() for obj in objs]}, 200

    @authorized(roles=["admin"])
    @valid_object(
        Datapoint,
        roles=["view", "admin"],
        DependentTypes=[DatasetVersion, Dataset],
        JoinBy=DatasetVersionDatapoint,
        id_field="datapoint_id",
    )
    @valid_object(
        Model,
        roles=["view", "admin"],
        DependentTypes=[AlgorithmVersion, Algorithm],
        id_field="model_id",
    )
    def post(self, datapoint_id: str, model_id: str) -> ResponseType:
        form = ResultForm(self.t, request.get_json() or {})
        if not form.validate():
            return {"message": "invalid data", "errors": form.errors}, 400
        with settings.session() as session:
            obj = Result(**form.valid_data)
            dpmr = DatapointModelResult(
                datapoint=request.datapoint, model=request.model, result=obj
            )
            session.add(dpmr)
            session.add(obj)
            session.commit()
            return obj.export(), 201
