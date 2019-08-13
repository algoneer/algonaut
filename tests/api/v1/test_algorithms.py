from algonaut.tests.helpers import MockApiTest

class TestAlgorithms(MockApiTest):
    def test_example(self):
        result = self.app.get('/v1/algorithms')
        assert result.status_code == 200