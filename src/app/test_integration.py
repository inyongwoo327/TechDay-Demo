import os
import subprocess
import time
import requests
import unittest

# Configuration for the integration test
S3_ENDPOINT = "http://localhost:4566"
DYNAMODB_ENDPOINT = "http://localhost:4566"
S3_BUCKET_NAME = "test-bucket"
DYNAMODB_TABLE_NAME = "test-table1"
FLASK_APP_URL = "http://localhost:5000"


def start_docker_compose():
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
    print("Docker Compose started.")
    time.sleep(10)  # Allow time for services to start


def stop_docker_compose():
    subprocess.run(["docker", "compose", "down"], check=True)
    print("Docker Compose stopped.")


def create_dynamodb_table():
    """Create the DynamoDB table using the awslocal CLI command."""
    command = [
        "awslocal", "dynamodb", "create-table",
        "--table-name", DYNAMODB_TABLE_NAME,
        "--attribute-definitions", "AttributeName=Id,AttributeType=S",
        "--key-schema", "AttributeName=Id,KeyType=HASH",
        "--provisioned-throughput", "ReadCapacityUnits=5,WriteCapacityUnits=5",
        "--endpoint-url", DYNAMODB_ENDPOINT
    ]
    subprocess.run(command, check=True)
    print(f"DynamoDB table '{DYNAMODB_TABLE_NAME}' created.")
    time.sleep(5)  # Allow time for table creation


def check_localstack_health():
    response = requests.get(f"{S3_ENDPOINT}/_localstack/health")
    if response.status_code == 200:
        print("LocalStack is healthy.")
    else:
        raise Exception("LocalStack is not healthy!")


def test_flask_app():
    response = requests.get(f"{FLASK_APP_URL}/")
    if response.status_code == 200:
        print("Flask app is responding.")
    else:
        raise Exception("Flask app is not responding!")


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        # Start the services and verify health
        start_docker_compose()
        check_localstack_health()
        test_flask_app()

        # Create the DynamoDB table using the CLI command
        create_dynamodb_table()

    def tearDown(self):
        stop_docker_compose()

    def test_store_data(self):
        """Test storing data via Flask app."""
        data = {"Id": "123", "name": "Test Name"}

        # Store data using the Flask endpoint
        response = requests.post(f"{FLASK_APP_URL}/store", json=data)
        print("Store response:", response.json())
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "Data stored successfully")
        print("Data successfully stored.")

    def test_retrieve_data(self):
        """Test retrieving data via Flask app."""
        data = {"Id": "123", "name": "Test Name"}

        # Store data first
        store_response = requests.post(f"{FLASK_APP_URL}/store", json=data)
        print("Store response:", store_response.json())
        self.assertEqual(store_response.status_code, 200)

        # Retrieve data
        retrieve_response = requests.get(f"{FLASK_APP_URL}/retrieve", params={"Id": "123"})
        print("Retrieve response:", retrieve_response.json())
        self.assertEqual(retrieve_response.status_code, 200)
        response_data = retrieve_response.json()
        expected_data = {"Id": "123", "name": "Test Name"}
        self.assertEqual(response_data, expected_data)
        print("Data successfully retrieved.")


if __name__ == "__main__":
    unittest.main()
