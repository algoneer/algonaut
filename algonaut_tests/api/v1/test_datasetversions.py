from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
import datetime
from algonaut_tests.fixtures.dataset import (
    dataset,
    datasetversion,
)

from .helpers import ObjectTest


class TestDatasetVersions(MockApiTest, ObjectTest):

    base_url = "/v1/datasets/{dataset.ext_id}/versions"
    obj_key = "datasetversion"
    obj_create_data = {"data": {"foo": "bar"}}
    obj_update_data = {"data": {"bar": "bam"}}

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"dataset": lambda test, fixtures: dataset(test, fixtures, "example")},
        {
            "datasetversion": lambda test, fixtures: datasetversion(
                test, fixtures, "dataset"
            )
        },
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "dataset"
            )
        },
    ]
