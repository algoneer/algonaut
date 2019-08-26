from algonaut_tests.helpers import DatabaseTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
from algonaut.models import ObjectRole
from algonaut_tests.fixtures.algorithm import project


class TestCreateObjectRole(DatabaseTest):

    """
    Test listing of projects
    """

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"project": lambda test, fixtures: project(test, fixtures, "example")},
    ]

    def test_create_role(self):
        obj_role = ObjectRole.get_or_create(
            self.session, self.project, self.organization, "admin", "admin"
        )
        self.session.commit()
        assert obj_role.id is not None
        same_obj_role = ObjectRole.get_or_create(
            self.session, self.project, self.organization, "admin", "admin"
        )
        self.session.commit()
        assert same_obj_role.id == obj_role.id
