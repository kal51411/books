# NyayaGPT Architecture

```mermaid
flowchart TD
  U[User] --> F[Next.js Frontend]
  F --> API[FastAPI API]
  API --> Guard[Prompt Injection Guard]
  Guard --> QU[Query Understanding]
  QU --> R[Hybrid Retrieval]
  R --> BM25[PostgreSQL BM25 / ts_rank]
  R --> V[Qdrant Vector Search]
  R --> M[Metadata Filters]
  BM25 --> RR[Cross Encoder Reranker]
  V --> RR
  M --> RR
  RR --> C[Context Builder]
  C --> LLM[Provider Router: OpenAI Anthropic Gemini Llama]
  LLM --> CV[Citation Validator]
  CV --> S[Safety Agent]
  S --> A[Traceable Answer]
```

## Multi-agent graph

Safety Agent → Retrieval Agent → Legal Research Agent → Case Law Agent → Final Answer Agent → Citation Verification Agent.

## Evidence invariant

The backend rejects responses when retrieval evidence is empty or when a citation does not map to an existing `(document_id, chunk_id, paragraph)` tuple.
