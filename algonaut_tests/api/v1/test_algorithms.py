from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
from algonaut_tests.fixtures.algorithm import (
    algorithm,
    algorithmversion,
    algorithmschema,
    algorithmversion_algorithmschema,
)


class TestAlgorithms(MockApiTest):

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

    def test_list(self):
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

    def test_valid_get(self):
        result = self.app.get(
            "/v1/algorithms/{}".format(self.algorithm.ext_id),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200
        algorithm = result.json
        assert isinstance(algorithm, dict)

    def test_invalid_get(self):
        result = self.app.get(
            "/v1/algorithms/{}".format(self.another_algorithm.ext_id),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 404

    def test_create(self):
        data = {
            "path": "my/example/algo",
            "description": "test",
            "data": {"foo": "bar"},
        }
        result = self.app.post(
            "/v1/algorithms", headers={"Authorization": "bearer test"}, json=data
        )
        assert result.status_code == 201
        algo = result.json
        assert "id" in algo

        for key, value in data.items():
            assert algo[key] == value
        result = self.app.get(
            "/v1/algorithms/{}".format(algo["id"]),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200

    def test_delete(self):

        result = self.app.get(
            "/v1/algorithms/{}".format(self.algorithm.ext_id),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200

        result = self.app.delete(
            "/v1/algorithms/{}".format(self.algorithm.ext_id),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200

        result = self.app.get(
            "/v1/algorithms/{}".format(self.algorithm.ext_id),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 404

    def test_update(self):

        data = {
            "path": "my/example/algo",
            "description": "test",
            "data": {"foo": "bar"},
        }
        for key, value in data.items():
            update_data = {key: value}
            result = self.app.patch(
                "/v1/algorithms/{}".format(self.algorithm.ext_id),
                headers={"Authorization": "bearer test"},
                json=update_data,
            )
            assert result.status_code == 200
            self.session.add(self.algorithm)
            self.session.refresh(self.algorithm)
            assert getattr(self.algorithm, key) == value
