# we import all relevant models

from .algorithmversion import AlgorithmVersion  # noqa
from .algorithm import Algorithm  # noqa
from .algorithmschema import AlgorithmSchema  # noqa
from .algorithmversion_algorithmschema import AlgorithmVersionAlgorithmSchema  # noqa
from .algorithmversion_result import AlgorithmVersionResult  # noqa
from .datapoint import Datapoint  # noqa
from .dataschema import DataSchema  # noqa
from .dataset import Dataset  # noqa
from .datasetversion_dataschema import DatasetVersionDataSchema  # noqa
from .datasetversion_datapoint import DatasetVersionDatapoint  # noqa
from .datasetversion_result import DatasetVersionResult  # noqa
from .datasetversion import DatasetVersion  # noqa
from .model_result import ModelResult  # noqa
from .model import Model  # noqa
from .result import Result  # noqa
from .object_role import ObjectRole  # noqa


def clean_db(session):
    engine = session.connection().engine
    for model in [
        AlgorithmVersionAlgorithmSchema,
        AlgorithmVersionResult,
        AlgorithmVersion,
        AlgorithmSchema,
        Algorithm,
        DatasetVersionDatapoint,
        DatasetVersionResult,
        DatasetVersionDataSchema,
        DatasetVersion,
        DataSchema,
        Datapoint,
        Dataset,
        ModelResult,
        Result,
        Model,
        ObjectRole,
    ]:
        engine.execute(model.__table__.delete())
