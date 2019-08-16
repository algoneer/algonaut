# we import all relevant models

from .algorithmversion import AlgorithmVersion
from .algorithm import Algorithm
from .algorithmschema import AlgorithmSchema
from .algorithmversion_algorithmschema import AlgorithmVersionAlgorithmSchema
from .algorithmversion_result import AlgorithmVersionResult
from .datapoint import DataPoint
from .dataschema import DataSchema
from .dataset import DataSet
from .datasetversion_dataschema import DataSetVersionDataSchema
from .datasetversion_datapoint import DataSetVersionDataPoint
from .datasetversion_result import DataSetVersionResult
from .datasetversion import DataSetVersion
from .model_result import ModelResult
from .model import Model
from .result import Result
from .object_role import ObjectRole


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
