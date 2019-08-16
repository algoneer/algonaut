from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client
from algonaut_tests.fixtures.algorithm import algorithm, algorithmversion


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
    ]

    def test_get(self):
        result = self.app.get(
            "/v1/algorithms", headers={"Authorization": "bearer test"}
        )
        assert result.status_code == 200
