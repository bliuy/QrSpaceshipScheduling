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
        self.assertEqual(response.status_code, 200)

        ## Asserting the content of the response
        expected_result = {"income": 18, "path": ["contract1", "contract3"]}
        actual_result = json.loads(response.content)
        self.assertEqual(expected_result, actual_result)

    def test_missing_contract_name(self):
        # Arrange
        payload = {
            "contracts_list": [
                {"name": "", "start": 0, "duration": 5, "price": 10},
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
        self.assertEqual(response.status_code, 422)

    def test_negative_start_times(self):
        # Arrange
        payload = {
            "contracts_list": [
                {"name": "contract1", "start": 0, "duration": 5, "price": 10},
                {"name": "contract2", "start": -3, "duration": 7, "price": 14},
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
        self.assertEqual(response.status_code, 422)

    def test_negative_duration(self):
        # Arrange
        payload = {
            "contracts_list": [
                {"name": "contract1", "start": 0, "duration": 5, "price": 10},
                {"name": "contract2", "start": 3, "duration": 7, "price": 14},
                {"name": "contract3", "start": 5, "duration": -9, "price": 8},
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
        self.assertEqual(response.status_code, 422)

    def test_zero_prices(self):
        # Arrange
        payload = {
            "contracts_list": [
                {"name": "contract1", "start": 0, "duration": 5, "price": 0},
                {"name": "contract2", "start": 3, "duration": 7, "price": 0},
                {"name": "contract3", "start": 5, "duration": 9, "price": 0},
                {"name": "contract4", "start": 5, "duration": 9, "price": 0},
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
        self.assertEqual(response.status_code, 422)

    def test_same_contract_names(self):
        # Arrange
        payload = {
            "contracts_list": [
                {"name": "contract1", "start": 0, "duration": 5, "price": 10},
                {"name": "contract1", "start": 3, "duration": 7, "price": 14},
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
        self.assertEqual(response.status_code, 422)

    def test_single_contract(self):
        # Arrange
        payload = {
            "contracts_list": [
                {"name": "contract1", "start": 0, "duration": 5, "price": 10},
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
        self.assertEqual(response.status_code, 200)

        ## Asserting the content of the response
        expected_result = {"income": 10, "path": ["contract1"]}
        actual_result = json.loads(response.content)
        self.assertEqual(expected_result, actual_result)

    def test_empty_payload(self):
        # Arrange
        payload = {
            "contracts_list": []
        }

        # Act
        response: httpx.Response = self.client.post(
            "/spaceship/optimize",
            headers={"Content-Type": "application/json"},
            json=payload,
        )

        # Assert

        ## Asserting the status code
        self.assertEqual(response.status_code, 422)

    def test_same_contract_conditions(self):
        # Arrange
        payload = {
            "contracts_list": [
                {"name": "contract1", "start": 0, "duration": 5, "price": 10},
                {"name": "contract2", "start": 0, "duration": 5, "price": 10},
                {"name": "contract3", "start": 0, "duration": 5, "price": 10},
                {"name": "contract4", "start": 0, "duration": 5, "price": 10},
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
        self.assertEqual(response.status_code, 200)

        ## Asserting the content of the response
        expected_result = {"income": 10, "path": ["contract1"]}
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
