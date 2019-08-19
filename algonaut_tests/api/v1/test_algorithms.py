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

    """
    Test listing of algorithms
    """

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"algorithm": lambda test, fixtures: algorithm(test, fixtures, "example")},
        # the next algorithm is not visible to the user
        {
            "another_algorithm": lambda test, fixtures: algorithm(
                test, fixtures, "another_example"
            )
        },
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

    def test_get_list(self):
        result = self.app.get(
            "/v1/algorithms", headers={"Authorization": "bearer test"}
        )
        assert result.status_code == 200
        algorithms = result.json
        assert isinstance(algorithms, dict)
        assert "data" in algorithms
        l = algorithms["data"]
        assert len(l) == 1
        algorithm = l[0]
        assert algorithm["path"] == "example"

    def test_valid_get_details(self):
        result = self.app.get(
            "/v1/algorithms/{}".format(self.algorithm.ext_id),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200
        algorithm = result.json
        assert isinstance(algorithm, dict)

    def test_invalid_get_details(self):
        result = self.app.get(
            "/v1/algorithms/{}".format(self.another_algorithm.ext_id),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 404
