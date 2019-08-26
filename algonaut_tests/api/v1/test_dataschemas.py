from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
from algonaut_tests.fixtures.dataset import dataset, dataschema, dataset_dataschema
from algonaut_tests.fixtures.algorithm import project
from .helpers import ObjectTest


class TestDataSchemas(MockApiTest, ObjectTest):

    base_url = "/v1/datasets/{dataset.ext_id}/schemas"
    obj_key = "dataschema"
    obj_create_data = {"data": {"foo": "bar"}}
    obj_update_data = {"data": {"bar": "bam"}}

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"project": project},
        {"dataset": dataset},
        {"dataschema": dataschema},
        {"dataset_dataschema": dataset_dataschema},
        {
            "object_role": lambda test, fixtures: object_role(
                test, fixtures, "admin", "admin", "organization", "project"
            )
        },
    ]
