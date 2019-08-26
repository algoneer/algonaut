from typing import List, Dict, Tuple, Any, Type
from ..resource import Resource

from .resources.project import Projects, ProjectDetails
from .resources.algorithmschema import AlgorithmSchemas, AlgorithmSchemaDetails
from .resources.algorithm import Algorithms, AlgorithmDetails
from .resources.result import (
    AlgorithmResults,
    AlgorithmResultDetails,
    ModelResults,
    ModelResultDetails,
    DatasetResults,
    DatasetResultDetails,
    DatapointModelResults,
    DatapointModelResultDetails,
)
from .resources.dataset import Datasets, DatasetDetails
from .resources.datapoint import Datapoints, DatapointDetails
from .resources.organization import Organizations
from .resources.model import CreateModel, AlgorithmModels, ModelDetails, DatasetModels
from .resources.object_role import ObjectRoles, ObjectRoleDetails
from .resources.dataschema import DataSchemas, DataSchemaDetails

routes: List[Dict[str, Tuple[Type[Resource], Dict[str, Any]]]] = [
    {"/organizations": (Organizations, {"methods": ["GET"]})},
    {"/projects": (Projects, {"methods": ["GET"]})},
    {"/projects/<organization_id>": (Projects, {"methods": ["POST"]})},
    {
        "/projects/<object_id>": (
            ProjectDetails,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
    {"/projects/<object_id>/algorithms": (Algorithms, {"methods": ["GET", "POST"]})},
    {
        "/algorithms/<object_id>": (
            AlgorithmDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {
        "/algorithms/<object_id>/schemas": (
            AlgorithmSchemas,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/algorithms/<dependent_id>/schemas/<object_id>": (
            AlgorithmSchemaDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {
        "/datapoints/<datapoint_id>/models/<model_id>/results": (
            DatapointModelResults,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/models/<dependent_id>/datapointresults/<object_id>": (
            DatapointModelResultDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {
        "/algorithms/<object_id>/results": (
            AlgorithmResults,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/algorithms/<dependent_id>/results/<object_id>": (
            AlgorithmResultDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {"/datasets/<object_id>/results": (DatasetResults, {"methods": ["GET", "POST"]})},
    {
        "/datasets/<dependent_id>/results/<object_id>": (
            DatasetResultDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {"/models/<object_id>/results": (ModelResults, {"methods": ["GET", "POST"]})},
    {
        "/models/<dependent_id>/results/<object_id>": (
            ModelResultDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {"/projects/<object_id>/datasets": (Datasets, {"methods": ["GET", "POST"]})},
    {
        "/datasets/<object_id>": (
            DatasetDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {"/datasets/<object_id>/datapoints": (Datapoints, {"methods": ["GET", "POST"]})},
    {
        "/datasets/<dependent_id>/datapoints/<object_id>": (
            DatapointDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {"/algorithms/<object_id>/models": (AlgorithmModels, {"methods": ["GET"]})},
    {"/models/<object_id>": (ModelDetails, {"methods": ["GET", "PATCH", "DELETE"]})},
    {
        "/datasets/<dataset_id>/algorithms/<algorithm_id>/models": (
            CreateModel,
            {"methods": ["POST"]},
        )
    },
    {"/datasets/<object_id>/models": (DatasetModels, {"methods": ["GET"]})},
    {"/objectroles": (ObjectRoles, {"methods": ["GET", "POST"]})},
    {
        "/objectroles/<object_id>": (
            ObjectRoleDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {"/datasets/<object_id>/schemas": (DataSchemas, {"methods": ["GET", "POST"]})},
    {
        "/datasets/<dependent_id>/schemas/<object_id>": (
            DataSchemaDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
]
