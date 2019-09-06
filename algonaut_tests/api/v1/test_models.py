from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
import datetime
from algonaut_tests.fixtures.algorithm import project, algorithm
from algonaut_tests.fixtures.model import model
from algonaut_tests.fixtures.dataset import dataset
from algonaut_tests.fixtures.result import model_result

from .helpers import ObjectTest


class TestAlgorithmModels(MockApiTest, ObjectTest):

    base_url = "/v1/models"
    obj_key = "model"
    obj_create_data = {"data": {"foo": "bar"}}
    obj_update_data = {"data": {"bar": "bam"}}

    @property
    def list_url(self):
        return "/v1/algorithms/{}/models".format(self.algorithm.ext_id)

    @property
    def create_url(self):
        return "/v1/datasets/{}/algorithms/{}/models".format(
            self.dataset.ext_id, self.algorithm.ext_id
        )

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"project": lambda test, fixtures: project(test, fixtures, "example")},
        {"algorithm": lambda test, fixtures: algorithm(test, fixtures, "project")},
        {"dataset": lambda test, fixtures: dataset(test, fixtures, name="foo/bar")},
        {"model": model},
        {"model_result": model_result},
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "project"
            )
        },
    ]

    def _create(self, data):
        ds = self.dataset
        av = self.algorithm
        return self.app.post(
            "/v1/datasets/{}/algorithms/{}/models".format(ds.ext_id, av.ext_id),
            headers={"Authorization": "bearer test"},
            json=data,
        )


class TestDatasetModels(TestAlgorithmModels):

    base_url = "/v1/models"

    @property
    def list_url(self):
        return "/v1/datasets/{}/models".format(self.dataset.ext_id)

    @property
    def create_url(self):
        return "/v1/datasets/{}/algorithms/{}/models".format(
            self.dataset.ext_id, self.algorithm.ext_id
        )
