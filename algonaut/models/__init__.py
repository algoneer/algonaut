# we import all relevant models

from .algorithm import Algorithm  # noqa
from .project import Project  # noqa
from .algorithmschema import AlgorithmSchema  # noqa
from .algorithm_algorithmschema import AlgorithmAlgorithmSchema  # noqa
from .algorithm_result import AlgorithmResult  # noqa
from .datapoint import Datapoint  # noqa
from .dataschema import DataSchema  # noqa
from .dataset import Dataset  # noqa
from .dataset_dataschema import DatasetDataSchema  # noqa
from .dataset_datapoint import DatasetDatapoint  # noqa
from .dataset_result import DatasetResult  # noqa
from .dataset import Dataset  # noqa
from .datapoint_model_result import DatapointModelResult  # noqa
from .model_result import ModelResult  # noqa
from .model import Model  # noqa
from .result import Result  # noqa
from .object_role import ObjectRole  # noqa
from .organization import Organization  # noqa
from .base import Base  # noqa


def clean_db(session):
    engine = session.connection().engine
    for model in [
        AlgorithmAlgorithmSchema,
        AlgorithmResult,
        DatapointModelResult,
        ModelResult,
        Model,
        Algorithm,
        AlgorithmSchema,
        DatasetDatapoint,
        DatasetResult,
        DatasetDataSchema,
        DataSchema,
        Datapoint,
        Dataset,
        Result,
        ObjectRole,
        Project,
        Organization,
    ]:
        engine.execute(model.__table__.delete())
