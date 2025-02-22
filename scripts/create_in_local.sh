#!/bin/bash

# Create an S3 bucket
awslocal s3api create-bucket --bucket test-bucket1 --create-bucket-configuration LocationConstraint=eu-west-1

# Create a DynamoDB table
awslocal dynamodb create-table \
    --table-name test-table1 \
    --attribute-definitions AttributeName=Id,AttributeType=S \
    --key-schema AttributeName=Id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

echo "Local AWS resources created!"
