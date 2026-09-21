# Centralized Observability Stack

Local Kubernetes project using Prometheus, Grafana, Loki, Promtail, Alertmanager, Helm, and a Flask metrics demo.

## Prerequisites
- Docker Desktop with WSL integration
- kubectl
- kind
- Helm

## Run
```bash
kind create cluster --name observability
kubectl apply -f k8s/namespace.yaml
docker build -t observability-demo:local ./app
kind load docker-image observability-demo:local --name observability
kubectl apply -f k8s/
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace -f helm/kube-prometheus-stack-values.yaml
helm upgrade --install loki grafana/loki -n monitoring -f helm/loki-values.yaml
helm upgrade --install promtail grafana/promtail -n monitoring -f helm/promtail-values.yaml
```

## Access
```bash
kubectl -n monitoring port-forward svc/monitoring-grafana 3000:80
kubectl -n monitoring get secret monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 -d; echo
```
Open http://localhost:3000 (user: admin).

Prometheus:
```bash
kubectl -n monitoring port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090
```

Application:
```bash
kubectl -n observability port-forward svc/observability-demo 8080:80
curl http://localhost:8080/health
curl http://localhost:8080/metrics
```

## Cleanup
```bash
helm uninstall promtail -n monitoring
helm uninstall loki -n monitoring
helm uninstall monitoring -n monitoring
kind delete cluster --name observability
```
