from algonaut_tests.helpers import DatabaseTest
from algonaut_tests.fixtures.user import user, auth_client, organization
from algonaut_tests.fixtures.object_role import object_role
from algonaut.models import Datapoint, DatasetDatapoint
from algonaut_tests.fixtures.algorithm import project
from algonaut_tests.fixtures.dataset import dataset

from sqlalchemy import func
from sqlalchemy.dialects import postgresql


class TestBulkInserts(DatabaseTest):

    """
    Test bulk insertion of datapoints.
    """

    fixtures = [
        {"auth_client": auth_client},
        {"organization": organization},
        {"user": user},
        {"project": lambda test, fixtures: project(test, fixtures, "example")},
        {"dataset": dataset},
    ]

    def test_bulk_inserts(self):
        dps = []
        dsdps = []
        ds = self.dataset
        n = 100
        for i in range(n):
            dp = Datapoint(data={"i": i})
            dps.append(dp)
        self.session.bulk_save_objects(dps, return_defaults=True)
        for i, dp in enumerate(dps):
            dsdp = DatasetDatapoint(dataset_id=ds.id, datapoint_id=dp.id)
            dsdps.append(dsdp)
        self.session.bulk_save_objects(dsdps, return_defaults=True)
        self.session.commit()
        assert self.session.query(Datapoint).count() == n
        assert self.session.query(DatasetDatapoint).count() == n

    def test_upserts(self):
        """
        * We first upsert 1000 datapoints into the database.
        * Then we associate them with a given dataset.
        * We repeat this two times to ensure it works.
        """
        ds = self.dataset
        n = 100
        for j in range(2):
            dsdps = []
            dps = []
            for i in range(n):
                dp = {"data": {"i": i}, "hash": "sdfdsfsdf{}".format(i).encode("utf-8")}
                dps.append(dp)
            ids = self.session.execute(
                postgresql.insert(Datapoint.__table__)
                .values(dps)
                .on_conflict_do_update(
                    set_={"updated_at": func.now()},
                    index_elements=[Datapoint.hash],
                    index_where=Datapoint.deleted_at == None,
                )
                .returning(Datapoint.id)
            )
            for i, id in enumerate(ids):
                dsdps.append({"dataset_id": ds.id, "datapoint_id": id[0]})
            self.session.commit()
            ids = self.session.execute(
                postgresql.insert(DatasetDatapoint.__table__)
                .values(dsdps)
                .on_conflict_do_update(
                    set_={"updated_at": func.now()},
                    index_elements=[
                        DatasetDatapoint.dataset_id,
                        DatasetDatapoint.datapoint_id,
                    ],
                    index_where=Datapoint.deleted_at == None,
                )
                .returning(DatasetDatapoint.id)
            )
        # we ensure the datapoints have been correctly inserted
        assert self.session.query(Datapoint).count() == n
        assert self.session.query(DatasetDatapoint).count() == n
