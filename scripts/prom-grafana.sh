#!/bin/bash
echo "This setup is to deploy prometheus and grafana only"

echo "###########helm prometheus installation begin#######"
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/prometheus -f ../prometheus-grafana/values.yml

echo "Helm grafana installation begins"
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install grafana grafana/grafana

echo "############retrieving the grafana dashboard password###########"
pass=$(kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 -d)
echo "the root password for grafana dashboard is: $pass"
echo "the user is: admin"
