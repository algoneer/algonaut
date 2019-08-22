from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
import datetime
from algonaut_tests.fixtures.algorithm import (
    algorithm,
    algorithmversion,
    algorithmschema,
    algorithmversion_algorithmschema,
)

from .helpers import ObjectTest


class TestAlgorithmVersions(MockApiTest, ObjectTest):

    base_url = "/v1/algorithmversions"
    obj_key = "algorithmversion"
    obj_create_data = {"data": {"foo": "bar"}}
    obj_update_data = {"data": {"bar": "bam"}}

    @property
    def list_url(self):
        return "/v1/algorithms/{}/versions".format(self.algorithm.ext_id)

    @property
    def create_url(self):
        return self.list_url

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
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "algorithm"
            )
        },
    ]
