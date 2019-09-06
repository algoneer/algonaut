from algonaut.models import (
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
DatasetResults = Objects(DatasetResult, ResultForm, [Dataset, Project])
DatasetResultDetails = ObjectDetails(DatasetResult, ResultForm, [Dataset, Project])

# Returns results for a given algorithm version
AlgorithmResults = Objects(AlgorithmResult, ResultForm, [Algorithm, Project])
AlgorithmResultDetails = ObjectDetails(
    AlgorithmResult, ResultForm, [Algorithm, Project]
)

# Returns results for a given model version
ModelResults = Objects(ModelResult, ResultForm, [Model, Algorithm, Project])
ModelResultDetails = ObjectDetails(ModelResult, ResultForm, [Model, Algorithm, Project])

DatapointModelResultDetails = ObjectDetails(
    DatapointModelResult, ResultForm, [Model, Algorithm, Project]
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
                DatapointModelResult.deleted_at == None,
                DatapointModelResult.datapoint == request.datapoint,
                DatapointModelResult.model == request.model,
            ]
            objs = session.query(DatapointModelResult).filter(*filters).all()
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
            obj = DatapointModelResult(**form.valid_data)
            obj.datapoint = request.datapoint
            obj.model = request.model

            session.expunge(obj)

            existing_obj = obj.get_existing(session)
            # if a matching result already exists we do not create a new one
            if existing_obj:

                # we update the existing object instead
                update_form = ResultForm(request.get_json() or {}, is_update=True)
                if not update_form.validate():
                    return {"message": "invalid data", "errors": form.errors}, 400

                for k, v in update_form.valid_data.items():
                    setattr(existing_obj, k, v)

                session.commit()

                return existing_obj.export(), 201

            session.add(obj)
            session.commit()
            return obj.export(), 201


DatasetModelResultDetails = ObjectDetails(
    DatasetModelResult, ResultForm, [Model, Algorithm, Project], DatasetModelResult
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
                DatasetModelResult.deleted_at == None,
                DatasetModelResult.dataset == request.dataset,
                DatasetModelResult.model == request.model,
            ]
            objs = session.query(DatasetModelResult).filter(*filters).all()
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
            obj = DatasetModelResult(**form.valid_data)

            obj.dataset = request.dataset
            obj.model = request.model

            session.expunge(obj)

            existing_obj = obj.get_existing(session)

            if existing_obj:

                # we update the existing object instead
                update_form = ResultForm(request.get_json() or {}, is_update=True)
                if not update_form.validate():
                    return {"message": "invalid data", "errors": form.errors}, 400

                for k, v in update_form.valid_data.items():
                    setattr(existing_obj, k, v)

                session.commit()

                return obj.export(), 201

            session.add(obj)
            session.commit()
            return obj.export(), 201
