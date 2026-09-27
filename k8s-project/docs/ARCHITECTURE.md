# Architecture Notes

## Flow
Developer pushes code -> CI builds Docker image -> image pushed to ACR ->
CD deploys via Helm to AKS (staging, then production behind a manual
approval gate) -> app runs behind NGINX Ingress with TLS -> Prometheus
scrapes metrics -> Grafana visualizes them -> HPA reacts to load.

## Why each layer exists
- **Docker**: packages the app and its exact dependencies into one
  portable, immutable artifact.
- **Kubernetes**: keeps the desired number of app copies running,
  restarts failed ones, and load-balances traffic between them.
- **Helm**: turns the raw YAML into a reusable, parameterized package
  so the same chart deploys to dev/staging/prod with different values.
- **Terraform**: provisions the cloud infrastructure (cluster, registry,
  networking) itself, so the environment is reproducible and version
  controlled, not clicked together in a portal.
- **Pipelines**: remove manual deploy steps, enforce that every change
  goes through build -> test -> staging -> approval -> production.
- **Monitoring**: without it you're blind to whether the app is actually
  healthy after a deploy, or why it's slow.
- **Security (RBAC/NetworkPolicy)**: limits blast radius if a pod or
  credential is compromised.

## Environments
This scaffold assumes 3 environments: dev (local/minikube), staging,
production — separated by Kubernetes namespace or by cluster, and by
distinct Helm value overrides + separate CI/CD approval gates.
