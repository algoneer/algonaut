from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
import datetime
from algonaut_tests.fixtures.algorithm import project, algorithm
from algonaut_tests.fixtures.model import model
from algonaut_tests.fixtures.dataset import dataset
from algonaut_tests.fixtures.result import result, model_result

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
        return self.list_url

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"project": lambda test, fixtures: project(test, fixtures, "example")},
        {"algorithm": lambda test, fixtures: algorithm(test, fixtures, "project")},
        {"dataset": lambda test, fixtures: dataset(test, fixtures, name="foo/bar")},
        {"model": model},
        {"result": lambda t, f: result(t, f, name="test")},
        {"model_result": model_result},
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "project"
            )
        },
    ]

    def test_create(self):
        """
        We overwrite the create test since models require two dependent
        objects (an algorithm and a dataset) to be created,
        so we need to pass both things in explicitly.
        """
        data = self.obj_create_data
        ds = self.dataset
        av = self.algorithm
        result = self.app.post(
            "/v1/datasets/{}/algorithms/{}/models".format(ds.ext_id, av.ext_id),
            headers={"Authorization": "bearer test"},
            json=data,
        )
        assert result.status_code == 201
        obj = result.json
        assert "id" in obj

        for key, value in data.items():
            assert obj[key] == value
        result = self.app.get(
            "{}/{}".format(self.url, obj["id"]),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200


class TestDatasetModels(TestAlgorithmModels):

    base_url = "/v1/models"

    @property
    def list_url(self):
        return "/v1/datasets/{}/models".format(self.dataset.ext_id)

    @property
    def create_url(self):
        return self.list_url
