# Deployment Guide

## Local

```bash
cp .env.example .env
docker compose -f infrastructure/docker/docker-compose.yml up --build
```

## Production

1. Provision PostgreSQL, Redis, Qdrant, object storage, Kubernetes, secret manager, and observability.
2. Store provider keys in KMS/Secret Manager; never bake secrets into images.
3. Run migrations and ingestion workers before exposing `/api/v1/ask`.
4. Deploy backend replicas with readiness probes and HPA.
5. Enable Prometheus scraping and Grafana dashboards.
