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
    DatasetVersionResults,
    DatasetVersionResultDetails,
    DatapointModelResults,
    DatapointModelResultDetails,
)
from .resources.dataset import Datasets, DatasetDetails
from .resources.datasetversion import DatasetVersions, DatasetVersionDetails
from .resources.datapoint import Datapoints, DatapointDetails
from .resources.organization import Organizations
from .resources.model import (
    CreateModel,
    AlgorithmModels,
    ModelDetails,
    DatasetVersionModels,
)
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
    {
        "/datasetversions/<object_id>/results": (
            DatasetVersionResults,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/datasetversions/<dependent_id>/results/<object_id>": (
            DatasetVersionResultDetails,
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
    {"/datasets": (Datasets, {"methods": ["GET"]})},
    {"/datasets/<organization_id>": (Datasets, {"methods": ["POST"]})},
    {
        "/datasets/<object_id>": (
            DatasetDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {"/datasets/<object_id>/versions": (DatasetVersions, {"methods": ["GET", "POST"]})},
    {
        "/datasetversions/<object_id>": (
            DatasetVersionDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {
        "/datasetversions/<object_id>/datapoints": (
            Datapoints,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/datasetversions/<dependent_id>/datapoints/<object_id>": (
            DatapointDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {"/algorithms/<object_id>/models": (AlgorithmModels, {"methods": ["GET"]})},
    {"/models/<object_id>": (ModelDetails, {"methods": ["GET", "PATCH", "DELETE"]})},
    {
        "/datasetversions/<datasetversion_id>/algorithms/<algorithm_id>/models": (
            CreateModel,
            {"methods": ["POST"]},
        )
    },
    {
        "/datasetversions/<object_id>/models": (
            DatasetVersionModels,
            {"methods": ["GET"]},
        )
    },
    {"/objectroles": (ObjectRoles, {"methods": ["GET", "POST"]})},
    {
        "/objectroles/<object_id>": (
            ObjectRoleDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {
        "/datasetversions/<object_id>/schemas": (
            DataSchemas,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/datasetversions/<dependent_id>/schemas/<object_id>": (
            DataSchemaDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
]
