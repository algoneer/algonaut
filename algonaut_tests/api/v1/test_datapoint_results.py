from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
import datetime
from algonaut_tests.fixtures.algorithm import algorithm, algorithmversion
from algonaut_tests.fixtures.model import model
from algonaut_tests.fixtures.dataset import (
    dataset,
    datasetversion,
    datapoint,
    datasetversion_datapoint,
)
from algonaut_tests.fixtures.result import result, datapoint_model_result

from .helpers import ObjectTest


class TestDatapointResults(MockApiTest, ObjectTest):

    base_url = "/v1/datapoints/{datapoint.ext_id}/results"
    obj_key = "result"
    obj_create_data = {"data": {"foo": "bar"}, "name": "test"}
    obj_update_data = {"data": {"bar": "bam"}, "name": "bar"}

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"algorithm": lambda test, fixtures: algorithm(test, fixtures, "example")},
        {
            "algorithmversion": lambda test, fixtures: algorithmversion(
                test, fixtures, "algorithm"
            )
        },
        {"dataset": lambda test, fixtures: dataset(test, fixtures, path="foo/bar")},
        {"datasetversion": datasetversion},
        {"datapoint": datapoint},
        {"datasetversion_datapoint": datasetversion_datapoint},
        {"model": model},
        {"result": lambda t, f: result(t, f, name="test")},
        {"datapoint_model_result": datapoint_model_result},
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "algorithm"
            )
        },
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "dataset"
            )
        },
    ]

    @property
    def url(self):
        model = self.model
        return "/v1/models/{}/datapointresults".format(model.ext_id)

    @property
    def list_url(self):
        dp = self.datapoint
        model = self.model
        return "/v1/datapoints/{}/models/{}/results".format(dp.ext_id, model.ext_id)

    @property
    def create_url(self):
        return self.list_url
