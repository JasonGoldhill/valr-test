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
The API can also be deployed to a GKE instance running in the `valr-test` GCP project (access to this project can be provided if required) using the `Build and Deploy` workflow in this repo. This workflow uses Terraform Cloud (again, access can be provided if required) to build the GKE instance if it doesn't already exist. It then uses a combination of `docker`, `gcloud` and `kubectl` to build and push the Docker image to a remote registry and then create our Kubernetes Deployment and Service.

To deploy the API to GKE:
1. Raise a PR from `develop` into `main`
2. Wait for the three Continuous Integration checks to pass successfully
3. Merge the PR
4. Navigate to the Actions tab in the repo and select the currently running `Build and Deploy` workflow
5. Wait for both the `Terraform Apply` and `Docker and Kubernetes` jobs to complete successfully
6. Grab the ip address for the Kubernetes Service from the output of the `Get svc ip address` step in the `Docker and Kubernetes` job
7. Navigate to `<ip address>:5000` to access the API

NOTE: Please run the `Destroy` workflow once done using the API in order to destroy the created GKE instance. To run the `Destroy` workflow:
1. Navigate to the Actions tab in the repo
2. Select the `Destroy` workflow from the list on the left
3. Click the `Run workflow` dropdown
4. Click the `Run workflow` button

# API Usage
The API has 3 available endpoints:

## 1. /orderbook/<pair> [GET]
This endpoint returns the orderbook for the provided pair in JSON format.

Example request:
```bash
curl --location --request GET 'localhost:5000/orderbook/BTCZAR'
```
Example response:
```bash
{
  "Asks": [
    {
      "price": 700001, 
      "quantity": 1
    }, 
    {
      "price": 700002, 
      "quantity": 1
    }, 
    {
      "price": 700003, 
      "quantity": 1
    }
  ], 
  "Bids": [
    {
      "price": 700000, 
      "quantity": 1
    }, 
    {
      "price": 699999, 
      "quantity": 1
    }, 
    {
      "price": 699998, 
      "quantity": 1
    }, 
    {
      "price": 699997, 
      "quantity": 1
    }
  ]
}
```

## 2. /tradeHistory/<pair> [GET]
This endpoint returns the trade history for the provided pair in JSON format. It can also accept an optional `limit` query parameter to limit the number of results returned.

Example request:
```bash
curl --location --request GET 'localhost:5000/tradeHistory/btczar?limit=3'
```

Example Response:
```bash
{
  "TradeHistory": [
    {
      "price": 699998, 
      "quantity": 1, 
      "takerSide": "sell"
    }, 
    {
      "price": 699999, 
      "quantity": 1, 
      "takerSide": "sell"
    }, 
    {
      "price": 700000, 
      "quantity": 1, 
      "takerSide": "sell"
    }
  ]
}
```

## 3. /limitOrder [POST]
This endpoint places a limit order into the orderbook. It requires the `side`, `pair`, `price` and `quantity` of the order to be passed through in the body of the request in JSON format. It also takes an optional additional parameter in the request body called `postOnly` (boolean) which determines whether the order should be cancelled or not if it matches.

Example request:
```bash
curl --location --request POST 'localhost:5000/limitOrder' \
--header 'Content-Type: application/json' \
--data-raw '{
    "side": "BUY",
    "quantity": 0.1,
    "price": 700000,
    "pair": "BTCZAR",
    "postOnly": false
}'
```
Example response (if order did not match):
```
Order placed.
```
Example response (if order matched and partially filled):
```
Order partially filled. Remainder placed in orderbook.
```
Example response (if order matched and completely filled):
```
Order completely filled.
```
Example response (if `postOnly=true` stopped order from filling):
```
Post Only order cancelled as it would have matched.
```
