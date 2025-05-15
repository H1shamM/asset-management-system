
# How to Recreate the System

## Start the kind Cluster

```bash
kind create cluster --name dev-cluster
```

## Build Your Docker Images

```bash
docker build -t asset-management-system-asset-service:v0.1.0 ./asset-service
docker build -t asset-management-system-security-service:v0.1.0 ./security-service
```

## Load Images into the Cluster

```bash
kind load docker-image asset-management-system-asset-service:v0.1.0 --name dev-cluster
kind load docker-image asset-management-system-security-service:v0.1.0 --name dev-cluster
```

## Apply Kubernetes Manifests

```bash
kubectl apply -f k8s-manifests/
```

## Verify Deployments and Services

```bash
kubectl get deployments
kubectl get pods
kubectl get svc
```

## Access Services Locally

```bash
kubectl port-forward svc/asset-service 5000:5000
kubectl port-forward svc/security-service 8080:8080
```

# How to Tear Down the System

## Delete Kubernetes Resources

```bash
kubectl delete -f k8s-manifests/
```

## Delete the kind Cluster

```bash
kind delete cluster --name dev-cluster
```

## Optional: Remove Local Docker Images

```bash
docker rmi asset-management-system-asset-service:v0.1.0
docker rmi asset-management-system-security-service:v0.1.0
```
