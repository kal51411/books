"""Prometheus metrics for latency, token usage, retrieval quality, and citation failures."""

from prometheus_client import Counter, Histogram

REQUEST_LATENCY = Histogram("nyayagpt_request_latency_seconds", "API request latency", ["route"])
RETRIEVAL_RESULTS = Histogram("nyayagpt_retrieval_results", "Number of retrieved chunks")
TOKEN_USAGE = Counter("nyayagpt_token_usage_total", "LLM token usage", ["provider", "model", "kind"])
FAILED_CITATIONS = Counter("nyayagpt_failed_citations_total", "Failed citation validations")
PROMPT_INJECTIONS = Counter("nyayagpt_prompt_injection_blocks_total", "Blocked prompt injections")
