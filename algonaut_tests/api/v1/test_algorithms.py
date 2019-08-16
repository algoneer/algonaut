from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
from algonaut_tests.fixtures.algorithm import (
    algorithm,
    algorithmversion,
    algorithmschema,
    algorithmversion_algorithmschema,
)


class TestGetAlgorithms(MockApiTest):

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
        {"algorithmschema": lambda test, fixtures: algorithmschema(test, fixtures)},
        {
            "algorithmversion_algorithmschema": lambda test, fixtures: algorithmversion_algorithmschema(
                test,
                fixtures,
                algoversion="algorithmversion",
                algoschema="algorithmschema",
            )
        },
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "algorithm"
            )
        },
    ]

    def test_get(self):
        result = self.app.get(
            "/v1/algorithms", headers={"Authorization": "bearer test"}
        )
        assert result.status_code == 200
        algorithms = result.json
        assert len(algorithms) == 1
        algorithm = algorithms[0]
        assert algorithm["path"] == "example"
