# Prerequisites
1. Docker
2. Local Kubernetes instance (e.g. Docker Desktop, Minikube, MicroK8s, etc.)
3. kubectl

# Local Deployment

First, build the Docker image by running the following command from the the project root:

```bash
docker build . -t valr-test
```
Next, making sure your Kubernetes conext is set correctly to your local instance, run the following command to create your Kubernetes Deployment:
```bash
kubectl apply -f k8s/deployment.yaml
```
Finally, create your Kubernetes Service by running:
```bash
kubectl apply -f k8s/service.yaml
```
The API should now be up and running! Depending on the setup of your local Kubernetes cluster you should now be able to access the API at `localhost:5000`. If not, you can try port-forwarding the service to your localhost by running:
```bash
kubectl port-forward svc/api-service 5000:5000
```

# GKE Deployment
The API can also be deployed to a GKE instance running in the `valr-test` GCP project (access to this project can be provided if required) using the CI/CD workflow in this repo.

This workflow uses Terraform Cloud (again, access can be provided if required) to build the GKE instance if it doesn't already exist. It then uses a combination of `docker`, `gcloud` and `kubectl` to build and push the Docker image to a remote registry and then create our Kubernetes Deployment and Service.

To use the workflow, simply raise a PR against `main`, which will run a `terraform plan` and allow you to see what changes will be made. Then merge the PR to run `terraform apply` and deploy the API to the cluster.
