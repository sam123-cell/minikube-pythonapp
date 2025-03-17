#!/bin/bash
echo "This setup is to deploy the reader application only"

echo "building the docker image"
docker build -f ../reader-app/Dockerfile -t mysql-reader:1.0 ../reader-app/

echo "loading the image to minkube"
minikube image load mysql-reader:1.0

echo "applying the kubectl now"
kubectl apply -f ../reader-app/python_read.yaml
