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
from .resources.datapoint import Datapoints, DatapointDetails
from .resources.model import (
    AlgorithmModels,
    AlgorithmModelDetails,
    DatasetModels,
    DatasetModelDetails,
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
    {"/algorithmschemas": (AlgorithmSchemas, {"methods": ["GET", "POST"]})},
    {
        "/algorithmschemas/<object_id>": (
            AlgorithmSchemaDetails,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
    {
        "/algorithmversions/<dependent_id>/results": (
            AlgorithmResults,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/algorithmversions/<dependent_id>/results/<object_id>": (
            AlgorithmResultDetails,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
    {
        "/datasetversions/<dependent_id>/results": (
            DatasetResults,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/datasetversions/<dependent_id>/results/<object_id>": (
            DatasetResultDetails,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
    {"/models/<dependent_id>/results": (ModelResults, {"methods": ["GET", "POST"]})},
    {
        "/models/<dependent_id>/results/<object_id>": (
            ModelResultDetails,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
    {"/datasets": (Datasets, {"methods": ["GET", "POST"]})},
    {
        "/dataset/<object_id>": (
            DatasetDetails,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
    {"/datasets/<dependent_id>/datapoints": (Datapoints, {"methods": ["GET", "POST"]})},
    {
        "/datasets/<dependent_id>/datapoints/<object_id>": (
            Datapoints,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
    {
        "/algorithmversions/<dependent_id>/models": (
            AlgorithmModels,
            {"methods": ["GET", "POST"]},
        )
    },
    {
        "/algorithmversions/<dependent_id>/models/<object_id>": (
            AlgorithmModelDetails,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
    {"/datasets/<dependent_id>/models": (DatasetModels, {"methods": ["GET", "POST"]})},
    {
        "/datasets/<dependent_id>/models/<object_id>": (
            DatasetModelDetails,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
    {"/objectroles": (ObjectRoles, {"methods": ["GET", "POST"]})},
    {
        "/objectroles/<object_id>": (
            ObjectRoleDetails,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
    {"/dataschemas": (DataSchemas, {"methods": ["GET", "POST"]})},
    {
        "/dataschemas/<object_id>": (
            DataSchemaDetails,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
]
