from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
import datetime
from algonaut_tests.fixtures.algorithm import project
from algonaut_tests.fixtures.dataset import dataset
from algonaut_tests.fixtures.result import dataset_result

from .helpers import ObjectTest


class TestDatasetResults(MockApiTest, ObjectTest):

    base_url = "/v1/datasets/{dataset.ext_id}/results"
    obj_key = "dataset_result"
    obj_create_data = {"data": {"foo": "bar"}, "name": "test"}
    obj_update_data = {"data": {"bar": "bam"}, "name": "bar"}

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"project": lambda test, fixtures: project(test, fixtures, "example")},
        {"dataset": lambda test, fixtures: dataset(test, fixtures, name="foo/bar")},
        {"dataset_result": dataset_result},
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "project"
            )
        },
    ]
