from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
from algonaut_tests.fixtures.algorithm import (
    project,
    algorithm,
    algorithmschema,
    algorithm_algorithmschema,
)
from .helpers import ObjectTest


class TestAlgorithmSchemas(MockApiTest, ObjectTest):

    base_url = "/v1/algorithms/{algorithm.ext_id}/schemas"
    obj_key = "algorithmschema"
    obj_create_data = {"data": {"foo": "bar"}}
    obj_update_data = {"data": {"bar": "bam"}}

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"project": lambda test, fixtures: project(test, fixtures, "example")},
        {"algorithm": lambda test, fixtures: algorithm(test, fixtures, "project")},
        {"algorithmschema": lambda test, fixtures: algorithmschema(test, fixtures)},
        {
            "algorithm_algorithmschema": lambda test, fixtures: algorithm_algorithmschema(
                test, fixtures, algorithm="algorithm", algoschema="algorithmschema"
            )
        },
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "project"
            )
        },
    ]
