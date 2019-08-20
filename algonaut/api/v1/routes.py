from typing import List, Dict, Tuple, Any, Type
from ..resource import Resource

from .resources.algorithm import Algorithms, AlgorithmDetails
from .resources.algorithmschema import AlgorithmSchemas, AlgorithmSchemaDetails
from .resources.algorithmversion import AlgorithmVersions, AlgorithmVersionDetails
from .resources.result import (
    AlgorithmResults,
    AlgorithmResultDetails,
    ModelResults,
    ModelResultDetails,
    DatasetResults,
    DatasetResultDetails,
)
from .resources.dataset import Datasets, DatasetDetails
from .resources.datasetversion import DatasetVersions, DatasetVersionDetails
from .resources.datapoint import Datapoints, DatapointDetails
from .resources.model import (
    CreateModel,
    AlgorithmModels,
    AlgorithmModelDetails,
    DatasetVersionModels,
    DatasetVersionModelDetails,
)
from .resources.object_role import ObjectRoles, ObjectRoleDetails
from .resources.dataschema import DataSchemas, DataSchemaDetails

routes: List[Dict[str, Tuple[Type[Resource], Dict[str, Any]]]] = [
    {"/algorithms": (Algorithms, {"methods": ["GET", "POST"]})},
    {
        "/algorithms/<object_id>": (
            AlgorithmDetails,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
    {
        "/algorithms/<object_id>/versions": (
            AlgorithmVersions,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/algorithms/<dependent_id>/versions/<object_id>": (
            AlgorithmVersionDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {
        "/algorithmversions/<object_id>/schemas": (
            AlgorithmSchemas,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/algorithmversions/<dependent_id>/schemas/<object_id>": (
            AlgorithmSchemaDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {
        "/algorithmversions/<object_id>/results": (
            AlgorithmResults,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/algorithmversions/<dependent_id>/results/<object_id>": (
            AlgorithmResultDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {
        "/datasetversions/<object_id>/results": (
            DatasetResults,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/datasetversions/<dependent_id>/results/<object_id>": (
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
    {"/datasets": (Datasets, {"methods": ["GET", "POST"]})},
    {
        "/datasets/<object_id>": (
            DatasetDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {"/datasets/<object_id>/versions": (DatasetVersions, {"methods": ["GET", "POST"]})},
    {
        "/datasets/<dependent_id>/versions/<object_id>": (
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
    {"/algorithmversions/<object_id>/models": (AlgorithmModels, {"methods": ["GET"]})},
    {
        "/algorithmversions/<dependent_id>/models/<object_id>": (
            AlgorithmModelDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {
        "/datasetversions/<datasetversion_id>/algorithmversions/<algorithmversion_id>/models": (
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
    {
        "/datasetversions/<dependent_id>/models/<object_id>": (
            DatasetVersionModelDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {"/objectroles": (ObjectRoles, {"methods": ["GET", "POST"]})},
    {
        "/objectroles/<object_id>": (
            ObjectRoleDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
    {"/dataschemas": (DataSchemas, {"methods": ["GET", "POST"]})},
    {
        "/dataschemas/<object_id>": (
            DataSchemaDetails,
            {"methods": ["GET", "PATCH", "DELETE"]},
        )
    },
]
