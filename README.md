# minikube-pythonapp
**Introduction**
This project is consisting of two application writer and reader written in python to interact with MySQL database deployed as a pod cluster in kubernetes.Also this projects expose some HTTP endpoint for couting the rows in table and exposing a metric for grafana visualization.
As you follow the instruction on this document you can easily deploy the complete setup at your local machine.

**Prerequisites**
It is assumed the below comonents are already installed in your local machine
- minikube
- kubectl
- docker

1) **MySQL DB installation**
Please login/start you minikube/kubernetes cluster and run below commands for MySQL installation setup

### Add helm repo and helm installation for MySQL ###
- helm repo add bitpoke https://helm-charts.bitpoke.io
- helm install mysql-operator bitpoke/mysql-operator

### Install MYSQL cluster ###
- cd mysql-db
- kubectl apply -f cluster-secret.yaml
- kubectl apply -f cluster.yaml

please not down the decoded data of password in secret created above and use it for db login.
Above setup will create one master and one reader replica MySQL cluster and please note this is automatically replicated and replication setup at startup time so no need to worry about the replication and data loss

########################################################################################################################
 
 **Writer Application setup**
To setup the writer application you need to follow below steps
- create image from docker file
-  transfer the image from your local machine to minikube container (if you have minikube, I am following the setup for minikube as per tghe requirement only)
- Deploy the application to minikube

### create the image from dockerfile ###
- cd ../writer-app-
- docker build . -t mysql-writer:1.0
- minikube image load mysql-writer:1.0
- kubectl apply -f python_write.yaml

you will see now that your writer application is up after some seconds
you can check the logs of application to check if its writing the query logs or not
kubectl logs -f <writer-app pod name> 

 #########################################################################################################################
 
 **Reader Application setup**
To setup the writer application you need to follow below steps
- create image from docker file
- transfer the image from your local machine to minikube container (if you have minikube, I am following the setup for minikube as per tghe requirement only)
- Deploy the application to minikube

### create the image from dockerfile ###
- cd ../reader-app
- docker build . -t mysql-reader:1.0
- minikube image load mysql-reader:1.0
- kubectl apply -f python_read.yaml

you will see now that your writer application is up after some seconds
you can check the logs of application to check if its writing the query logs or not
kubectl logs -f <reader-app pod name>

#############################################################################################################################

 **Prometheus grafana setup**
For setting up prometheus and grafan you need to follow below steps.

### Add helm repo and helm installation for Prometheus ###
- helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
- helm repo update
- helm install prometheus prometheus-community/prometheus

### Add helm repo and helm installation for Grafana ###
- helm repo add grafana https://grafana.github.io/helm-charts 
- helm repo update
- helm install grafana grafana/grafana

Now add the scrap configurations for response query endpoints for both writer and reader application in prometheus configmap
kubectl edit cm prometheus-server
find the scrap config section in configmap and add below lines just below **scrape_configs:**
scrape_configs:
- job_name: 'sql-metrics-reader'
  metrics_path: /metrics
  static_configs:
    - targets: ['mysql-reader-service.default.svc.cluster.local:5000']
- job_name: 'sql-metrics-writer'
  metrics_path: /metrics
  static_configs:
    - targets: ['mysql-writer-service.default.svc.cluster.local:80']
 
Restart the prometheus server by applying below command
kubectl rollout restart deployment prometheus-server

Now your metrics endpoints for both reader and writer app will be scraped by prometheus

##############################################################################################################################

**Configure the Grafana dashboard**
apply below command to access grafana dashboard
- kubectl port-forward svc/grafana 8081:80

- browse localhost:8081 in your browser and use admin as username and get the password from below command
- kubectl get secret --namespace default grafana -o yaml
- try to look for admin-password: under data section and decode the value using base64 and use the password now.
- Once logged in Click on Add data source and select Prometheus as Data source
- give it a name and paste http://prometheus-server.default.svc.cluster.local on connection block and save it.
- once logged in click on Dashboard and new Dashboard
- click on Add Visualization
- select prometheus data source created above
- on the left hand select mysql_query_response_time_miliseconds_writer as metric and paste mysql_query_response_time_miliseconds_writer in the query section and give it a name of the panel as per your choice
- save it and you will see writer metrics in this panel
- follow the same for reader as well using mysql_query_response_time_miliseconds and metric and query
