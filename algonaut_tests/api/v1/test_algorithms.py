from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client
from algonaut_tests.fixtures.algorithm import (
    algorithm,
    algorithmversion,
    algorithmschema,
    algorithmversion_algorithmschema,
)


class TestGetAlgorithms(MockApiTest):

    fixtures = [
        {"auth_client": auth_client},
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
    ]

    def test_get(self):
        result = self.app.get(
            "/v1/algorithms", headers={"Authorization": "bearer test"}
        )
        assert result.status_code == 200
