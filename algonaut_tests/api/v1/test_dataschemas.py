from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
from algonaut_tests.fixtures.dataset import (
    dataset,
    datasetversion,
    dataschema,
    datasetversion_dataschema,
)
from .helpers import ObjectTest


class TestDataSchemas(MockApiTest, ObjectTest):

    base_url = "/v1/datasetversions/{datasetversion.ext_id}/schemas"
    obj_key = "dataschema"
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
        {"dataschema": lambda test, fixtures: dataschema(test, fixtures)},
        {
            "datasetversion_dataschema": lambda test, fixtures: datasetversion_dataschema(
                test, fixtures, dsversion="datasetversion", dsschema="dataschema"
            )
        },
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "dataset"
            )
        },
    ]
