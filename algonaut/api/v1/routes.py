from typing import List, Dict, Tuple, Any, Type
from ..resource import Resource

from .resources.algorithm import Algorithms, AlgorithmDetails
from .resources.algorithmschema import AlgorithmSchemas, AlgorithmSchemaDetails
from .resources.algorithmversion import AlgorithmVersions, AlgorithmVersionDetails
from .resources.result import Results, ResultDetails
from .resources.dataset import Datasets, DatasetDetails
from .resources.datapoint import Datapoints, DatapointDetails
from .resources.model import Models, ModelDetails
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
    {"/results": (Results, {"methods": ["GET", "POST"]})},
    {
        "/results/<object_id>": (
            ResultDetails,
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
    {"/datapoints": (Datapoints, {"methods": ["GET", "POST"]})},
    {
        "/datapoints/<object_id>": (
            DatapointDetails,
            {"methods": ["GET", "POST", "PATCH", "DELETE"]},
        )
    },
    {"/models": (Models, {"methods": ["GET", "POST"]})},
    {
        "/models/<object_id>": (
            ModelDetails,
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
