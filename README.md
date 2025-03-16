# minikube-pythonapp
**Introduction**
This project is consisting of two application writer and reader written in python to interact with MySQL database deployed as a pod cluster in kubernetes.Also this projects expose some HTTP endpoint for couting the rows in table and exposing a metric for grafana visualization.
As you follow the instruction on this document you can easily deploy the complete setup at your local machine.

**Prerequisites**
It is assumed the below comonents are already installed in your local machine
a) minikube
b) kubectl
c) docker

1) **MySQL DB installation**
Please login/start you minikube/kubernetes cluster and run below commands for MySQL installation setup

### Add helm repon and helm installation for MySQL ###
a) helm repo add bitpoke https://helm-charts.bitpoke.io
b) helm install mysql-operator bitpoke/mysql-operator

### Install MYSQL cluster ###
cd mysql-db
a) kubectl apply -f cluster-secret.yaml
b) kubectl apply -f cluster.yaml

please not down tghe decoded data of password in secret created above and use it for db login.
Above setup will create one master and one reader replica MySQL cluster and please note this is automatically replicated and replication setup at startup time so no need to worry about the replication and data loss

2) **Writer Application setup**
To setup the writer application you need to follow below steps
a) create image from docker file
b) transfer the image from your local machine to minikube container (if you have minikube, I am following the setup for minikube as per tghe requirement only)
c) Deploy the application to minikube

### create the image from dockerfile ###
a) cd ../writer-app
b) docker build . -t mysql-writer:1.0
c) minikube image load mysql-writer:1.0
d) kubectl apply -f python_write.yaml

you will see now that your writer application is up after some seconds
you can check the logs of application to check if its writing the query logs or not
kubectl logs -f <writer-app pod name> 

3) **Reader Application setup**
3) To setup the writer application you need to follow below steps
a) create image from docker file
b) transfer the image from your local machine to minikube container (if you have minikube, I am following the setup for minikube as per tghe requirement only)
c) Deploy the application to minikube

### create the image from dockerfile ###
a) cd ../reader-app
b) docker build . -t mysql-reader:1.0
c) kubectl apply -f python_read.yaml

you will see now that your writer application is up after some seconds
you can check the logs of application to check if its writing the query logs or not
kubectl logs -f <reader-app pod name>

4) **Prometheus grafana setup**
For setting up prometheus and grafan you need to follow below steps.

### Add helm repo and helm installation for Prometheus ###
a) helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
b) helm repo update
c) helm install prometheus prometheus-community/prometheus

### Add helm repo and helm installation for Grafana ###
a) helm repo add grafana https://grafana.github.io/helm-charts 
b) helm repo update
c) helm install grafana grafana/grafana
