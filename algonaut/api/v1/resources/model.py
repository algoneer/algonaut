from algonaut.models import (
    Model,
    AlgorithmVersion,
    DatasetVersion,
    Dataset,
    Algorithm,
    ObjectRole,
)
from algonaut.api.resource import Resource, ResponseType
from algonaut.api.decorators import valid_object, authorized
from ..forms import ModelForm
from .object import Objects, ObjectDetails
from flask import request
from algonaut.settings import settings

# Returns models for a given dataset version
DatasetVersionModels = Objects(Model, ModelForm, [DatasetVersion, Dataset])

# Returns models for a given algorithm version
AlgorithmModels = Objects(Model, ModelForm, [AlgorithmVersion, Algorithm])
ModelDetails = ObjectDetails(Model, ModelForm, [AlgorithmVersion, Algorithm])


class CreateModel(Resource):
    @authorized(roles=["admin", "superuser"])
    @valid_object(
        AlgorithmVersion,
        roles=["view", "admin"],
        DependentTypes=[Algorithm],
        id_field="algorithmversion_id",
    )
    @valid_object(
        DatasetVersion,
        roles=["view", "admin"],
        DependentTypes=[Dataset],
        id_field="datasetversion_id",
    )
    def post(self, algorithmversion_id: str, datasetversion_id: str) -> ResponseType:
        form = ModelForm(self.t, request.get_json() or {})
        if not form.validate():
            return {"message": "invalid data", "errors": form.errors}, 400
        with settings.session() as session:
            obj = Model(**form.valid_data)
            obj.algorithmversion = request.algorithmversion
            obj.datasetversion = request.datasetversion
            session.add(obj)
            session.commit()
            return obj.export(), 201
