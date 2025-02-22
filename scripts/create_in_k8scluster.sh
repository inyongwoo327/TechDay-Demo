#!/bin/bash

# Create an S3 bucket
awslocal s3api create-bucket --bucket test-bucket2 --create-bucket-configuration LocationConstraint=eu-west-1 --endpoint-url http://localhost:4566

# Create a DynamoDB table
awslocal dynamodb create-table --table-name test-table2 --attribute-definitions AttributeName=Id,AttributeType=S --key-schema AttributeName=Id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 --endpoint-url http://localhost:4566

echo "Local AWS resources created!"
