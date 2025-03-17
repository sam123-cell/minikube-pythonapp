# minikube-pythonapp
**Introduction**
This project is consisting of two application writer and reader written in python to interact with MySQL database deployed as a pod cluster in kubernetes.Also this projects expose some HTTP endpoint for couting the rows in table and exposing a metric for grafana visualization.
As you follow the instruction on this document you can easily deploy the complete setup at your local machine.

**Prerequisites**
It is assumed the below comonents are already installed in your local machine
- minikube
- kubectl
- docker
- curl
  
if minikube is not installed then run below command on your linux machine

- cd scripts
- chmod +x minikube.sh
- ./minikube.sh
referenced the link (https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)
1) **MySQL DB installation**
Please login/start you minikube/kubernetes cluster and run below script for MySQL installation setup

- chmod +x mysql_script.sh
- ./mysql_script.sh

this will install mysql db setup and give you password for root user in mysql db please note down the decoded data of password in secret created above and use it for db login.
Above setup will create one master and one reader replica MySQL cluster and please note this is automatically replicated and replication setup at startup time so no need to worry about the replication and data loss

########################################################################################################################
 
 **Writer Application setup**
To setup the writer application you need to follow below steps
- create image from docker file
- transfer the image from your local machine to minikube container (if you have minikube, I am following the setup for minikube as per the requirement only)
- Deploy the application to minikube

### create the image from dockerfile ###
- chmod +x writer_script.sh
- ./writer_script.sh
- 
you will see now that your writer application is up after some seconds
you can check the logs of application to check if its writing the query logs or not
kubectl logs -f <writer-app pod name> 

 #########################################################################################################################
 
 **Reader Application setup**
To setup the writer application you need to follow below steps
- create image from docker file
- transfer the image from your local machine to minikube container (if you have minikube, I am following the setup for minikube as per tghe requirement only)
- Deploy the application to minikube

### create the image from dockerfile and deploy using below script ###
- chmod +x reader_script.sh
- ./reader_script.sh

you will see now that your reader application is up after some seconds
you can check the logs of application to check if its writing the query logs or not
kubectl logs -f <reader-app pod name>

run minikube tunnel on a separate terminal then use below endpoint for reader row count.
http endpoint for row count in reader app --> **http://localhost:5000/rows**
#############################################################################################################################

 **Prometheus grafana setup**
For setting up prometheus and grafan you need to follow below steps.

### Add helm repo and helm installation for Prometheus ###
- chmod +x prom-grafana.sh
- ./prom-grafana.sh

 above script execution will give you username and password for grafana dashboard login

Now your metrics endpoints for both reader and writer app also will be scraped by prometheus

##############################################################################################################################

**Configure the Grafana dashboard**
apply below command to access grafana dashboard
- kubectl port-forward svc/grafana 8080:80

- browse localhost:8080 in your browser and use admin as username and get the password from the script executed just above
- go to the data source and select prometheus as data source, give it a name and provide the connection URL as **http://prometheus-server.default.svc.cluster.local**
- now create a dashboard and click **ADD Visualization** and give the panel a name and save it
- once saved click on the three dots on upper right corner and click on Inspect --> Panel Json
- paste below files content there and save it.
  **query-response-time-writer.json**
  your writer dashboard is ready
- Follow the same process for point 3 for reader dashboard as well and use below file for import
  **query-response-time-reader.json**
