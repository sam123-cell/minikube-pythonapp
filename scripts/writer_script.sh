#!/bin/bash
echo "This setup is to deploy the writer application only"

echo "building the docker image"
docker build -f ../writer-app/Dockerfile -t mysql-write:1.0 ../writer-app/

echo "loading the image to minkube"
minikube image load mysql-writer:1.0

echo "applying the kubectl now"
kubectl apply -f ../writer-app/python_write.yaml
