from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
from algonaut_tests.fixtures.algorithm import project

from .helpers import ObjectTest


class TestProjects(MockApiTest, ObjectTest):

    base_url = "/v1/projects"

    obj_key = "project"
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

    @property
    def create_url(self):
        self.session.add(self.organization)
        return "{}/{}".format(self.base_url, self.organization.source_id.hex())

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {
            "another_organization": lambda test, fixtures: organization(
                test, fixtures, name="another one"
            )
        },
        {"user": user},
        {"project": lambda test, fixtures: project(test, fixtures, "example")},
        # the next project is not visible to the user
        {
            "another_project": lambda test, fixtures: project(
                test, fixtures, "another_example", "another_organization"
            )
        },
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "project"
            )
        },
    ]
