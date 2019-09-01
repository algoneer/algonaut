from algonaut.models import Model, Algorithm, Dataset, Project, ObjectRole
from algonaut.api.resource import Resource, ResponseType
from algonaut.api.decorators import valid_object, authorized
from ..forms import ModelForm
from .object import Objects, ObjectDetails
from flask import request
from algonaut.settings import settings

joins = [
    [Model.algorithm, Algorithm.project, Project.organization],
    [Model.dataset, Dataset.project, Project.organization],
]

# Returns models for a given dataset version
DatasetModels = Objects(Model, ModelForm, [Dataset, Project], Joins=joins)

# Returns models for a given algorithm version
AlgorithmModels = Objects(Model, ModelForm, [Algorithm, Project], Joins=joins)
ModelDetails = ObjectDetails(Model, ModelForm, [Algorithm, Project], Joins=joins)


class CreateModel(Resource):
    @authorized()
    @valid_object(
        Algorithm, roles=["admin"], DependentTypes=[Project], id_field="algorithm_id"
    )
    @valid_object(
        Dataset, roles=["admin"], DependentTypes=[Project], id_field="dataset_id"
    )
    def post(self, algorithm_id: str, dataset_id: str) -> ResponseType:
        form = ModelForm(request.get_json() or {})
        if not form.validate():
            return {"message": "invalid data", "errors": form.errors}, 400
        with settings.session() as session:
            obj = Model(**form.valid_data)

            existing_obj = (
                session.query(Model)
                .filter(
                    Model.algorithm_id == request.algorithm.id,
                    Model.dataset_id == request.dataset.id,
                    Model.hash == obj.hash,
                    Model.deleted_at == None,
                )
                .one_or_none()
            )
            if existing_obj:
                return existing_obj.export(), 201

            obj.algorithm = request.algorithm
            obj.dataset = request.dataset
            session.add(obj)

            session.commit()
            return obj.export(), 201
