from algonaut_tests.helpers import MockApiTest
from algonaut_tests.fixtures.user import user, auth_client

class TestAlgorithms(MockApiTest):

    fixtures = [{'auth_client' : auth_client}, {'user' : user}]

    def test_example(self):
        result = self.app.get('/v1/algorithms', headers={'Authorization' : 'bearer test'})
        assert result.status_code == 200