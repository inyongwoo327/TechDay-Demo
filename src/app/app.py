# src/app/app.py
from flask import Flask, jsonify, request
import boto3
import os

app = Flask(__name__)

# Localstack endpoint urls
"""
S3_ENDPOINT = "http://localhost:4566"
DYNAMODB_ENDPOINT = "http://localhost:4566"
"""

S3_ENDPOINT = os.getenv('S3_ENDPOINT', 'http://localhost:4566')
DYNAMODB_ENDPOINT = os.getenv('DYNAMODB_ENDPOINT', 'http://localhost:4566')

# AWS Region (required for boto3 to work)
AWS_REGION = "eu-west-1"
AWS_ACCESS_KEY = "test"
AWS_SECRET_KEY = "test"

# AWS clients
s3 = boto3.client('s3', endpoint_url=S3_ENDPOINT, region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
dynamodb = boto3.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT, region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

TABLE_NAME = 'test-table1'

@app.route('/')
def home():
    return "Welcome to the Techday!\n"

@app.route('/s3-buckets')
def list_s3_buckets():
    try:
        response = s3.list_buckets()
        return jsonify(response.get('Buckets', []))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dynamodb-tables')
def list_dynamodb_tables():
    try:
        tables = [table.name for table in dynamodb.tables.all()]
        return jsonify(tables)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store', methods=['POST'])
def store_data():
    try:
        # Parse JSON payload
        data = request.get_json()
        app.logger.info(f"Received raw data: {data}")

        # Validate payload
        if not data:
            app.logger.error("Payload is empty or invalid.")
            return jsonify({'error': 'Invalid JSON payload'}), 400
        if 'Id' not in data:
            app.logger.error(f"Missing 'Id' in payload: {data}")
            return jsonify({'error': 'Invalid payload. "Id" is required'}), 400

        # Insert data into DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item=data)
        app.logger.info(f"Data successfully stored: {data}")
        return jsonify({'message': 'Data stored successfully'}), 200
    except Exception as e:
        app.logger.error(f"Error in /store endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/retrieve', methods=['GET'])
def retrieve_data():
    try:
        # Retrieve the 'Id' parameter from the query string (case-sensitive)
        item_id = request.args.get('Id')  # Use 'Id' to match DynamoDB schema
        app.logger.info(f"Retrieving data for Id: {item_id}")

        if not item_id:
            app.logger.error("Missing 'Id' in query parameters.")
            return jsonify({'error': "'Id' query parameter is required"}), 400

        # Fetch the table from DynamoDB
        table = dynamodb.Table(TABLE_NAME)

        # Retrieve the item based on the key
        response = table.get_item(Key={'Id': item_id})  # Use 'Id' as the key

        # Check if the item exists in the response
        if 'Item' not in response:
            app.logger.warning(f"Item with Id '{item_id}' not found.")
            return jsonify({'error': 'Item not found'}), 404

        app.logger.info(f"Item retrieved: {response['Item']}")
        return jsonify(response['Item']), 200
    except Exception as e:
        app.logger.error(f"Error in /retrieve endpoint: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
