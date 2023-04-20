from fastapi.testclient import TestClient
import unittest
import typing
from unittest import mock
from src.main import app
import httpx
import json


class TestSpaceshipOptimize(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_example_query(self):
        # Arrange
        payload = {
            "contracts_list": [
                {"name": "contract1", "start": 0, "duration": 5, "price": 10},
                {"name": "contract2", "start": 3, "duration": 7, "price": 14},
                {"name": "contract3", "start": 5, "duration": 9, "price": 8},
                {"name": "contract4", "start": 5, "duration": 9, "price": 7},
            ]
        }

        # Act
        response: httpx.Response = self.client.post(
            "/spaceship/optimize",
            headers={"Content-Type": "application/json"},
            json=payload,
        )

        # Assert

        ## Asserting the status code
        self.assertEquals(response.status_code, 200)

        ## Asserting the content of the response
        expected_result = {"income": 18, "path": ["contract1", "contract3"]}
        actual_result = json.loads(response.content)
        self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    test_cases: typing.List = [
        TestSpaceshipOptimize,
    ]

    test_suites = [
        unittest.TestLoader().loadTestsFromTestCase(test) for test in test_cases
    ]

    all_tests = unittest.TestSuite(test_suites)

    runner = unittest.TextTestRunner()
    runner.run(all_tests)
