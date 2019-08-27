from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization


class TestOrganizations(MockApiTest):

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {
            "another_organization": lambda test, fixtures: organization(
                test, fixtures, name="another one"
            )
        },
        {"user": user},
    ]

    def test_list(self):
        result = self.app.get(
            "/v1/organizations", headers={"Authorization": "bearer test"}
        )
        assert result.status_code == 200
        objs = result.json
        assert isinstance(objs, dict)
        assert "data" in objs
        l = objs["data"]
        assert len(l) == 1
