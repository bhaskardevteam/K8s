# K8s Production Project

End-to-end example: containerized app -> Kubernetes -> Helm -> Terraform
(Azure) -> CI/CD -> monitoring. See `docs/ARCHITECTURE.md` for the theory.

## Repo layout
```
app/         Flask demo app (source code)
docker/      Dockerfile
k8s/         Raw Kubernetes manifests (good for learning each piece)
helm/        Helm chart that packages the k8s/ manifests, parameterized
terraform/   Provisions Azure resource group, ACR, AKS
pipelines/   CI/CD: Azure DevOps + GitHub Actions versions
monitoring/  Prometheus/Grafana config for the app
docs/        Architecture notes
```

## 1. Run locally (no cluster needed)
```bash
cd app
pip install -r requirements.txt
python main.py
# curl http://localhost:8080/
```

## 2. Build and run in Docker
```bash
docker build -f docker/Dockerfile -t k8s-demo-app:local .
docker run -p 8080:8080 k8s-demo-app:local
```

## 3. Provision Azure infra with Terraform
```bash
cd terraform
terraform init
terraform plan
terraform apply
```
This creates a resource group, an Azure Container Registry (ACR), and an
AKS cluster, and grants AKS pull access to ACR.

## 4. Point kubectl at the new cluster
```bash
az aks get-credentials --resource-group k8sdemo-rg --name k8sdemo-aks
```

## 5. Deploy — two ways

**a) Raw manifests (to learn what's happening):**
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
```

**b) Helm (how you'd actually run this in production):**
```bash
helm upgrade --install k8s-demo ./helm \
  --namespace k8s-demo --create-namespace \
  --set image.repository=<your-acr-name>.azurecr.io/k8s-demo-app \
  --set image.tag=latest
```

## 6. Install monitoring
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  -f monitoring/prometheus-values.yaml -n monitoring --create-namespace
kubectl apply -f monitoring/servicemonitor.yaml
```

## 7. Wire up CI/CD
Push this repo to GitHub or Azure DevOps and configure the pipeline in
`pipelines/`. It builds the Docker image, pushes to ACR, and runs
`helm upgrade` against staging, then production behind a manual gate.

## Verify
```bash
kubectl get pods -n k8s-demo
kubectl port-forward svc/k8s-demo-app 8080:80 -n k8s-demo
curl http://localhost:8080/health
```
