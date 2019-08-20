from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
from algonaut_tests.fixtures.dataset import dataset

from .helpers import ObjectTest


class TestDatasets(MockApiTest, ObjectTest):

    base_url = "/v1/datasets"
    obj_key = "dataset"
    obj_create_data = {
        "path": "example/algo",
        "data": {"foo": "bar"},
        "description": "",
        "tags": ["my", "tags"],
    }
    obj_update_data = {
        "path": "another/path",
        "data": {"bar": "baz"},
        "description": "foo",
        "tags": ["one", "two"],
    }

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"dataset": lambda test, fixtures: dataset(test, fixtures, "example")},
        # the next algorithm is not visible to the user
        {
            "another_dataset": lambda test, fixtures: dataset(
                test, fixtures, "another_example"
            )
        },
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "dataset"
            )
        },
    ]
