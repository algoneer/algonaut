from algonaut.models import (
    Model,
    Algorithm,
    DatasetVersion,
    Dataset,
    Project,
    ObjectRole,
)
from algonaut.api.resource import Resource, ResponseType
from algonaut.api.decorators import valid_object, authorized
from ..forms import ModelForm
from .object import Objects, ObjectDetails
from flask import request
from algonaut.settings import settings

joins = [
    [Model.algorithm, Algorithm.project, Project.organization],
    [Model.datasetversion, DatasetVersion.dataset, Dataset.organization],
]

# Returns models for a given dataset version
DatasetVersionModels = Objects(Model, ModelForm, [DatasetVersion, Dataset], Joins=joins)

# Returns models for a given algorithm version
AlgorithmModels = Objects(Model, ModelForm, [Algorithm, Project], Joins=joins)
ModelDetails = ObjectDetails(Model, ModelForm, [Algorithm, Project], Joins=joins)


class CreateModel(Resource):
    @authorized()
    @valid_object(
        Algorithm, roles=["admin"], DependentTypes=[Project], id_field="algorithm_id"
    )
    @valid_object(
        DatasetVersion,
        roles=["admin"],
        DependentTypes=[Dataset],
        id_field="datasetversion_id",
    )
    def post(self, algorithm_id: str, datasetversion_id: str) -> ResponseType:
        form = ModelForm(self.t, request.get_json() or {})
        if not form.validate():
            return {"message": "invalid data", "errors": form.errors}, 400
        with settings.session() as session:
            obj = Model(**form.valid_data)
            obj.algorithm = request.algorithm
            obj.datasetversion = request.datasetversion
            session.add(obj)
            session.commit()
            return obj.export(), 201
