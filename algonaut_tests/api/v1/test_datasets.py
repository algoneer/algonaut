from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
from algonaut_tests.fixtures.algorithm import project
from algonaut_tests.fixtures.dataset import dataset

from .helpers import ObjectTest


class TestDatasets(MockApiTest, ObjectTest):

    base_url = "/v1/datasets"
    obj_key = "dataset"
    obj_create_data = {
        "name": "example/algo",
        "data": {"foo": "bar"},
        "tags": ["my", "tags"],
    }
    obj_update_data = {
        "name": "another/path",
        "data": {"bar": "baz"},
        "tags": ["one", "two"],
    }

    @property
    def list_url(self):
        return "/v1/projects/{}/datasets".format(self.project.ext_id)

    @property
    def create_url(self):
        return self.list_url

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {
            "another_organization": lambda test, fixtures: organization(
                test, fixtures, name="another one"
            )
        },
        {"user": user},
        {"project": project},
        {
            "another_project": lambda test, fixtures: project(
                test, fixtures, "another/project", "another_organization"
            )
        },
        {"dataset": lambda test, fixtures: dataset(test, fixtures, "example")},
        # the next dataset is not visible to the user
        {
            "another_dataset": lambda test, fixtures: dataset(
                test, fixtures, "another_example", "another_project"
            )
        },
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "project"
            )
        },
    ]
