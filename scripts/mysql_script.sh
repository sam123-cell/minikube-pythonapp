#!/bin/bash
echo "This setup is to deploy mysql cluster only"

echo "###########helm installation begin#######"
helm repo add bitpoke https://helm-charts.bitpoke.io
helm install mysql-operator bitpoke/mysql-operator

echo "applying the kubectl now for cluster installation"
kubectl apply -f ../mysql-db/cluster-secret.yaml
kubectl apply -f ../mysql-db/cluster.yaml

echo "############retrieving the root password###########"
pass=$(kubectl get secret my-secret -o jsonpath="{.data.ROOT_PASSWORD}" | base64 -d)
echo "the root password for db is: $pass"
