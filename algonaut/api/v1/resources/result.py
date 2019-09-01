from algonaut.models import (
    Result,
    Model,
    ModelResult,
    Datapoint,
    DatasetDatapoint,
    DatasetModelResult,
    DatapointModelResult,
    AlgorithmResult,
    DatasetResult,
    Algorithm,
    Dataset,
    Project,
)
from ..forms import ResultForm
from .object import Objects, ObjectDetails

from algonaut.api.resource import Resource, ResponseType
from algonaut.api.decorators import valid_object, authorized
from algonaut.settings import settings
from flask import request

from typing import Optional

# Returns results for a given dataset version
DatasetResults = Objects(Result, ResultForm, [Dataset, Project], DatasetResult)
DatasetResultDetails = ObjectDetails(
    Result, ResultForm, [Dataset, Project], DatasetResult
)

# Returns results for a given algorithm version
AlgorithmResults = Objects(Result, ResultForm, [Algorithm, Project], AlgorithmResult)
AlgorithmResultDetails = ObjectDetails(
    Result, ResultForm, [Algorithm, Project], AlgorithmResult
)

# Returns results for a given model version
ModelResults = Objects(Result, ResultForm, [Model, Algorithm, Project], ModelResult)
ModelResultDetails = ObjectDetails(
    Result, ResultForm, [Model, Algorithm, Project], ModelResult
)

DatapointModelResultDetails = ObjectDetails(
    Result, ResultForm, [Model, Algorithm, Project], DatapointModelResult
)


class DatapointModelResults(Resource):
    @authorized()
    @valid_object(
        Datapoint,
        roles=["view", "admin"],
        DependentTypes=[Dataset, Project],
        JoinBy=DatasetDatapoint,
        id_field="datapoint_id",
    )
    @valid_object(
        Model,
        roles=["view", "admin"],
        DependentTypes=[Algorithm, Project],
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

    @authorized()
    @valid_object(
        Datapoint,
        roles=["admin"],
        DependentTypes=[Dataset, Project],
        JoinBy=DatasetDatapoint,
        id_field="datapoint_id",
    )
    @valid_object(
        Model, roles=["admin"], DependentTypes=[Algorithm, Project], id_field="model_id"
    )
    def post(self, datapoint_id: str, model_id: str) -> ResponseType:
        form = ResultForm(request.get_json() or {})
        if not form.validate():
            return {"message": "invalid data", "errors": form.errors}, 400
        with settings.session() as session:
            obj = Result(**form.valid_data)
            existing_obj = (
                session.query(Result)
                .filter(Result.hash == obj.hash, Result.deleted_at == None)
                .one_or_none()
            )

            # if a matching result already exists we do not create a new one
            if existing_obj:
                obj = existing_obj
            else:
                session.add(obj)
                session.commit()

            # we check if an existing entry already exists
            existing_obj = (
                session.query(DatapointModelResult)
                .filter(
                    DatapointModelResult.model_id == request.model.id,
                    DatapointModelResult.datapoint_id == request.datapoint.id,
                    DatapointModelResult.result_id == obj.id,
                    DatapointModelResult.deleted_at == None,
                )
                .one_or_none()
            )

            # we return the existing object without adding a M2M entry
            if existing_obj:
                return obj.export(), 201

            dpmr = DatapointModelResult(
                datapoint=request.datapoint, model=request.model, result=obj
            )
            session.add(dpmr)
            session.commit()
            return obj.export(), 201


DatasetModelResultDetails = ObjectDetails(
    Result, ResultForm, [Model, Algorithm, Project], DatasetModelResult
)


class DatasetModelResults(Resource):
    @authorized()
    @valid_object(
        Dataset,
        roles=["view", "admin"],
        DependentTypes=[Project],
        id_field="dataset_id",
    )
    @valid_object(
        Model,
        roles=["view", "admin"],
        DependentTypes=[Algorithm, Project],
        id_field="model_id",
    )
    def get(self, dataset_id: str, model_id: str) -> ResponseType:
        """
        Return all objects that match the given criteria and that the user is
        allowed to see.
        """
        with settings.session() as session:
            filters = [
                Result.deleted_at == None,
                DatasetModelResult.dataset == request.dataset,
                DatasetModelResult.model == request.model,
            ]
            objs = session.query(Result).filter(*filters).join(DatasetModelResult).all()
            return {"data": [obj.export() for obj in objs]}, 200

    @authorized()
    @valid_object(
        Dataset, roles=["admin"], DependentTypes=[Project], id_field="dataset_id"
    )
    @valid_object(
        Model, roles=["admin"], DependentTypes=[Algorithm, Project], id_field="model_id"
    )
    def post(self, dataset_id: str, model_id: str) -> ResponseType:
        form = ResultForm(request.get_json() or {})
        if not form.validate():
            return {"message": "invalid data", "errors": form.errors}, 400
        with settings.session() as session:
            obj = Result(**form.valid_data)
            existing_obj = (
                session.query(Result)
                .filter(Result.hash == obj.hash, Result.deleted_at == None)
                .one_or_none()
            )

            # if a matching result already exists we do not create a new one
            if existing_obj:
                obj = existing_obj
            else:
                session.add(obj)
                session.commit()

            # we check if an existing entry already exists
            existing_obj = (
                session.query(DatasetModelResult)
                .filter(
                    DatasetModelResult.model_id == request.model.id,
                    DatasetModelResult.dataset_id == request.dataset.id,
                    DatasetModelResult.result_id == obj.id,
                    DatasetModelResult.deleted_at == None,
                )
                .one_or_none()
            )

            # we return the existing object without adding a M2M entry
            if existing_obj:
                return obj.export(), 201

            dpmr = DatasetModelResult(
                dataset=request.dataset, model=request.model, result=obj
            )
            session.add(dpmr)
            session.commit()
            return obj.export(), 201
