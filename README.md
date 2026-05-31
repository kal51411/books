# NyayaGPT

**AI-Powered Indian Legal Research and Assistance Platform**

NyayaGPT is a production-oriented monorepo for Indian legal AI research and assistance. It combines a FastAPI backend, Next.js frontend, ingestion pipelines, evaluation harnesses, observability, security controls, and deployable infrastructure for evidence-grounded legal RAG.

> Legal safety invariant: NyayaGPT never returns legal analysis unless every claim is backed by validated retrieval evidence and citations.

## Monorepo

- `frontend/` — Next.js, TypeScript, Tailwind, shadcn-style UI shells.
- `backend/` — FastAPI, async service layer, provider-agnostic LLM abstraction, RAG graph, citation enforcement.
- `ingestion/` — PDF/OCR/metadata/chunk/embed/index pipeline for Indian statutes, judgments, rules, gazettes, and commentary.
- `evaluation/` — retrieval, generation, legal-accuracy metrics and dashboard artifacts.
- `infrastructure/` — Docker Compose, Kubernetes, Terraform, Prometheus/Grafana, CI workflow.
- `docs/` — architecture, API, database, deployment, evaluation, and security reports.
- `tests/` — cross-cutting API, security, and load test assets.

## Quick start

```bash
cp .env.example .env
docker compose -f infrastructure/docker/docker-compose.yml up --build
```

Backend: http://localhost:8000/docs
Frontend: http://localhost:3000
Grafana: http://localhost:3001
Qdrant: http://localhost:6333/dashboard

## Core RAG Flow

Query understanding → hybrid retrieval → cross-encoder reranking → context building → LLM answer → citation validation → safety review → final response.
