import abc
import datetime

from typing import Dict, Any


class ObjectTest(abc.ABC):

    base_url: str = ""
    obj_key: str = ""
    obj_create_data: Dict[str, Any] = {}
    obj_update_data: Dict[str, Any] = {}

    @property
    def url(self):
        return self.base_url.format(**self.fixture_objs)

    def test_list(self):
        result = self.app.get(self.url, headers={"Authorization": "bearer test"})
        assert result.status_code == 200
        objs = result.json
        assert isinstance(objs, dict)
        assert "data" in objs
        l = objs["data"]
        assert len(l) == 1
        obj = l[0]
        orig_obj = self.fixture_objs[self.obj_key]
        for key, value in obj.items():
            if key == "id":
                orig_value = str(orig_obj.ext_id)
            else:
                orig_value = getattr(orig_obj, key)
            if key in ("created_at", "updated_at", "deleted_at"):
                if orig_value is not None:
                    orig_value = datetime.datetime.strftime(
                        orig_value, "%Y-%m-%dT%H:%M:%SZ"
                    )
            assert value == orig_value

    def test_get(self):
        result = self.app.get(
            "{}/{}".format(self.url, self.fixture_objs[self.obj_key].ext_id),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200
        obj = result.json
        assert isinstance(obj, dict)

    def test_create(self):
        data = self.obj_create_data
        result = self.app.post(
            self.url, headers={"Authorization": "bearer test"}, json=data
        )
        print(result.status_code, self.url)
        assert result.status_code == 201
        obj = result.json
        assert "id" in obj

        for key, value in data.items():
            assert obj[key] == value
        result = self.app.get(
            "{}/{}".format(self.url, obj["id"]),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200

    def test_delete(self):

        result = self.app.get(
            "{}/{}".format(self.url, self.fixture_objs[self.obj_key].ext_id),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200

        result = self.app.delete(
            "{}/{}".format(self.url, self.fixture_objs[self.obj_key].ext_id),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 200

        result = self.app.get(
            "{}/{}".format(self.url, self.fixture_objs[self.obj_key].ext_id),
            headers={"Authorization": "bearer test"},
        )
        assert result.status_code == 404

    def test_update(self):

        data = self.obj_update_data
        obj = self.fixture_objs[self.obj_key]
        for key, value in data.items():
            update_data = {key: value}
            result = self.app.patch(
                "{}/{}".format(self.url, obj.ext_id),
                headers={"Authorization": "bearer test"},
                json=update_data,
            )
            assert result.status_code == 200
            self.session.add(obj)
            self.session.refresh(obj)
            assert getattr(obj, key) == value
