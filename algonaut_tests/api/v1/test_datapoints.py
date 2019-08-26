from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
from algonaut_tests.fixtures.algorithm import project
from algonaut_tests.fixtures.dataset import dataset, datapoint, dataset_datapoint
from .helpers import ObjectTest


class TestDatapoints(MockApiTest, ObjectTest):

    base_url = "/v1/datasets/{dataset.ext_id}/datapoints"
    obj_key = "datapoint"
    obj_create_data = {"data": {"foo": "bar"}}
    obj_update_data = {"data": {"bar": "bam"}}

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"project": project},
        {"dataset": lambda test, fixtures: dataset(test, fixtures, "example")},
        {"datapoint": datapoint},
        {"dataset_datapoint": dataset_datapoint},
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "project"
            )
        },
    ]
