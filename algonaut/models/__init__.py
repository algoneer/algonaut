# we import all relevant models

from .algorithmversion import AlgorithmVersion  # noqa
from .algorithm import Algorithm  # noqa
from .algorithmschema import AlgorithmSchema  # noqa
from .algorithmversion_algorithmschema import AlgorithmVersionAlgorithmSchema  # noqa
from .algorithmversion_result import AlgorithmVersionResult  # noqa
from .datapoint import DataPoint  # noqa
from .dataschema import DataSchema  # noqa
from .dataset import DataSet  # noqa
from .datasetversion_dataschema import DataSetVersionDataSchema  # noqa
from .datasetversion_datapoint import DataSetVersionDataPoint  # noqa
from .datasetversion_result import DataSetVersionResult  # noqa
from .datasetversion import DataSetVersion  # noqa
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
        DataSetVersionDataPoint,
        DataSetVersionResult,
        DataSetVersionDataSchema,
        DataSetVersion,
        DataSchema,
        DataPoint,
        DataSet,
        ModelResult,
        Result,
        Model,
        ObjectRole,
    ]:
        engine.execute(model.__table__.delete())
