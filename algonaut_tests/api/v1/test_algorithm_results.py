from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
import datetime
from algonaut_tests.fixtures.algorithm import project, algorithm
from algonaut_tests.fixtures.model import model
from algonaut_tests.fixtures.dataset import dataset
from algonaut_tests.fixtures.result import algorithm_result

from .helpers import ObjectTest


class TestAlgorithmResults(MockApiTest, ObjectTest):

    base_url = "/v1/algorithms/{algorithm.ext_id}/results"
    obj_key = "algorithm_result"
    obj_create_data = {"data": {"foo": "bars"}, "name": "another test"}
    obj_update_data = {"data": {"bar": "bam"}, "name": "bar"}

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"project": lambda test, fixtures: project(test, fixtures, "example")},
        {"algorithm": lambda test, fixtures: algorithm(test, fixtures, "project")},
        {"dataset": lambda test, fixtures: dataset(test, fixtures, name="foo/bar")},
        {"model": model},
        {"algorithm_result": algorithm_result},
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "project"
            )
        },
    ]
