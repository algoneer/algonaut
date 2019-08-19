from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
import datetime
from algonaut_tests.fixtures.algorithm import (
    algorithm,
    algorithmversion,
    algorithmschema,
    algorithmversion_algorithmschema,
)


class TestAlgorithmVersions(MockApiTest):

    """
    Test listing of algorithms
    """

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
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "algorithm"
            )
        },
    ]

    def test_list(self):
        result = self.app.get(
            "/v1/algorithms/{}/versions".format(self.algorithm.ext_id),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200
        algorithmversions = result.json
        assert isinstance(algorithmversions, dict)
        assert "data" in algorithmversions
        l = algorithmversions["data"]
        assert len(l) == 1
        algorithmversion = l[0]
        for key, value in algorithmversion.items():
            if key == "id":
                orig_value = str(self.algorithmversion.ext_id)
            else:
                orig_value = getattr(self.algorithmversion, key)
            if key in ("created_at", "updated_at", "deleted_at"):
                if orig_value is not None:
                    orig_value = datetime.datetime.strftime(
                        orig_value, "%Y-%m-%dT%H:%M:%SZ"
                    )
            assert value == orig_value

    def test_get(self):
        result = self.app.get(
            "/v1/algorithms/{}/versions/{}".format(
                self.algorithm.ext_id, self.algorithmversion.ext_id
            ),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200
        algorithm = result.json
        assert isinstance(algorithm, dict)

    def test_create(self):
        data = {"data": {"foo": "bar"}}
        result = self.app.post(
            "/v1/algorithms/{}/versions".format(self.algorithm.ext_id),
            headers={"Authorization": "bearer test"},
            json=data,
        )
        assert result.status_code == 201
        algo = result.json
        assert "id" in algo

        for key, value in data.items():
            assert algo[key] == value
        result = self.app.get(
            "/v1/algorithms/{}/versions/{}".format(self.algorithm.ext_id, algo["id"]),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200

    def test_delete(self):

        result = self.app.get(
            "/v1/algorithms/{}/versions/{}".format(
                self.algorithm.ext_id, self.algorithmversion.ext_id
            ),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200

        result = self.app.delete(
            "/v1/algorithms/{}/versions/{}".format(
                self.algorithm.ext_id, self.algorithmversion.ext_id
            ),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200

        result = self.app.get(
            "/v1/algorithms/{}/versions/{}".format(
                self.algorithm.ext_id, self.algorithmversion.ext_id
            ),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 404

    def test_update(self):

        data = {"data": {"foo": "bar"}}
        for key, value in data.items():
            update_data = {key: value}
            result = self.app.patch(
                "/v1/algorithms/{}/versions/{}".format(
                    self.algorithm.ext_id, self.algorithmversion.ext_id
                ),
                headers={"Authorization": "bearer test"},
                json=update_data,
            )
            assert result.status_code == 200
            self.session.add(self.algorithm)
            self.session.refresh(self.algorithm)
            assert getattr(self.algorithmversion, key) == value
