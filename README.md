
# flask-weather-knn-accuracy-microservice
Small Flask Microservice that uses sklearn knn to make a prediction of city's weather and calculate its accuracy.



## Architectural Diagram

## Assets in Repo

* `Makefile`:  [Builds project](https://github.com/nogibjj/Proj2-jl1188-kubernetes-flask-microservice/blob/main/Makefile)
* `Dockerfile`:  [Container configuration](https://github.com/nogibjj/Proj2-jl1188-kubernetes-flask-microservice/blob/main/Dockerfile)
* `app.py`:  [Flask app](https://github.com/nogibjj/Proj2-jl1188-kubernetes-flask-microservice/blob/main/app.py)
* `kube-rain-prediction.yaml`: [Kubernetes YAML Config](https://github.com/nogibjj/Proj2-jl1188-kubernetes-flask-microservice/blob/main/kube-rain-prediction.yaml)

## Get Started

* Create Python virtual environment `python3 -m venv ~/.kube-hello && source ~/.kube-hello/bin/activate`
* Run `make all` to install python libraries, lint project, including `Dockerfile` 


### Run the project local
(checklist: Github release)

* Python run it:  `python app.py`
* Invoke it.  `make invoke` (using curl)

## Build and Run Docker Container

* Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

* To build the image locally do the following.

`docker build -t rain-prediction:latest .` or run `make build` which has the same command.

* To verify container run `docker image ls`

* To run do the following:  `docker run -p 8080:8080 rain-prediction` or run `make run` which has the same command

* In a separate terminal invoke the web service via curl, or run `make invoke` which has the same command 
`curl http://127.0.0.1:8080/accuracy/Canberra`

```bash
{
  "accuracy": "0.868", 
  "name": "Canberra"
}
```

* Stop the running docker container by using `control-c` command

# Pushed Image to Docker Hub (fully workable)
* Pull with: `docker pull selinaliu/knn-rain-prediction-accuracy`

# Pushed Image to AWS ECR (not full workable)

* Pull with the following command: `docker pull public.ecr.aws/x2v3g2s0/flask-predict:latest`

* Run the docker image: `docker run -it --rm -p 8080:8080 public.ecr.aws/x2v3g2s0/flask-predict:latest`



## Running Kubernetes Locally
* Install [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/) and [Minikube](https://minikube.sigs.k8s.io/docs/start/)

* Start minikube cluster with `minikube start`

* Interact with cluster
  - If you already have kubectl installed: `kubectl get po -A`
  - Otherwise, minikube download kubectl for you `minikube kubectl -- get po -A`
  - Adding the alias `alias kubectl="minikube kubectl --"`

* Deploy
  - See the node by typing: `kubectl get nodes`

  - Create a deployment: `kubectl create deployment knn-predict --image=registry.hub.docker.com/selinaliu/knn-rain-prediction-accuracy` or run `make deploy` which have the same command
  ```bash
  deployment.apps/knn-predict created
  ```
  - View the deployments with: `kubectl get deployments`
  ```bash
  NAME          READY   UP-TO-DATE   AVAILABLE   AGE
  knn-predict   0/1     1            0           10s
  ```
  - Create service and expose it : `kubectl expose deployment knn-predict --type=LoadBalancer --port=8080`
  ```bash
  service/knn-predict exposed
  ```
  - View services: `kubectl get service knn-predict`
  ```bash
  NAME          TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
  knn-predict   LoadBalancer   10.101.152.34   <pending>     8080:32535/TCP   13s
  ```
  - `minikube service knn-predict --url`
  ```bash
  http://127.0.0.1:56821
  ❗  Because you are using a Docker driver on darwin, the terminal needs to be open to run it.
  ```
  - Curl web service in a new terminal: `curl http://127.0.0.1:56821/accuracy/Canberra`

* Invoke with `make invoke`

* Cleanup
- Delete the service `kubectl delete services knn-predict`
- Delete the deployment `kubectl delete deployment knn-predict`



### Continuous Integration Steps
- test
- format
- lint
- publish

### Benchmarking


### Logging, for Microservices




## Loadtest with Locust

* [Install Locust](https://github.com/locustio/locust)
* Create a `locustfile.py`
* Run loadtests
![Screen Shot 2021-03-16 at 3 02 59 PM](https://user-images.githubusercontent.com/58792/111367175-d7328600-866a-11eb-9a4d-3429710593ea.png)
![Screen Shot 2021-03-16 at 3 02 35 PM](https://user-images.githubusercontent.com/58792/111367176-d7328600-866a-11eb-9856-928d42e65a9a.png)
![Screen Shot 2021-03-16 at 3 01 22 PM](https://user-images.githubusercontent.com/58792/111367178-d7cb1c80-866a-11eb-8c29-6440a6179544.png)

## References

* Noah Gift example [Kubernetes Hello World](https://github.com/noahgift/kubernetes-hello-world-python-flask/)
* Noah Gift Flask Change [flask-change-microservice](https://github.com/noahgift/flask-change-microservice)
* create Kubernetes Service, YAML [Use a Service to Access an Application in a Cluster](https://kubernetes.io/docs/tasks/access-application-cluster/service-access-application-cluster/) 
* Step-by-step Guide [Get started with Kubernetes (using Python)](https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/)
* Kubernetes deployment from image in Dockerhub[coursera-applied-de-kubernetes-lab](https://github.com/nogibjj/coursera-applied-de-kubernetes-lab)



