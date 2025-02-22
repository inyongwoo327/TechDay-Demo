#!/bin/bash

# Create a service for LocalStack
kubectl create -f localstack-service.yaml

# Create a service for Flask App
kubectl create -f service.yml

# Create a deployment (pod) for Localstack
kubectl create -f localstack-deployment.yaml

# Create a deployment (pod) for Flask App
kubectl create -f deployment.yaml

echo "K8s Deployments (pods) and services are created!"
