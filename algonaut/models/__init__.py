# we import all relevant models

from .algorithm import Algorithm  # noqa
from .project import Project  # noqa
from .algorithmschema import AlgorithmSchema  # noqa
from .algorithm_algorithmschema import AlgorithmAlgorithmSchema  # noqa
from .algorithm_result import AlgorithmResult  # noqa
from .datapoint import Datapoint  # noqa
from .dataschema import DataSchema  # noqa
from .dataset import Dataset  # noqa
from .datasetversion_dataschema import DatasetVersionDataSchema  # noqa
from .datasetversion_datapoint import DatasetVersionDatapoint  # noqa
from .datasetversion_result import DatasetVersionResult  # noqa
from .datasetversion import DatasetVersion  # noqa
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
        Project,
        DatasetVersionDatapoint,
        DatasetVersionResult,
        DatasetVersionDataSchema,
        DatasetVersion,
        DataSchema,
        Datapoint,
        Dataset,
        Result,
        ObjectRole,
        Organization,
    ]:
        engine.execute(model.__table__.delete())
