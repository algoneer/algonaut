from algonaut.models import Datapoint, Dataset, Project, DatasetDatapoint
from algonaut.api.resource import Resource, ResponseType
from algonaut.api.decorators import valid_object, authorized

from algonaut.api.resource import Resource
from ..forms import DatapointForm
from .object import Objects, ObjectDetails

from flask import request

Datapoints = Objects(Datapoint, DatapointForm, [Dataset, Project], DatasetDatapoint)
DatapointDetails = ObjectDetails(
    Datapoint, DatapointForm, [Dataset, Project], DatasetDatapoint
)


class BulkDatapoints(Resource):
    @authorized()
    @valid_object(
        Dataset, roles=["admin"], DependentTypes=[Project], id_field="dataset_id"
    )
    def post(self, algorithm_id: str, dataset_id: str) -> ResponseType:
        return {}, 200
