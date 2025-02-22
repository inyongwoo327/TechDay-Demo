#!/bin/bash

# Script for setting up Kind and configuring Kubernetes

# Install Kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Create a Kubernetes cluster with Kind
kind create cluster --name localstack-cluster

# Set up Docker to work with Kind
export KUBECONFIG="$(kind get kubeconfig --name localstack-cluster)"

# Confirm cluster is running
kubectl cluster-info
