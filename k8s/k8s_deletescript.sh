#!/bin/bash

# Create a service for LocalStack
kubectl delete -f localstack-service.yaml

# Create a service for Flask App
kubectl delete -f service.yml

# Create a deployment (pod) for Localstack
kubectl delete -f localstack-deployment.yaml

# Create a deployment (pod) for Flask App
kubectl delete -f deployment.yaml

echo "K8s Deployments (pods) and services are delete!"
