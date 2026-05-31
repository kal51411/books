# Evaluation Report

NyayaGPT evaluates three layers:

| Layer | Metrics |
| --- | --- |
| Retrieval | Recall@K, MRR, NDCG |
| Generation | Faithfulness, groundedness, hallucination rate |
| Legal accuracy | Citation correctness, section correctness, case relevance |

Benchmark datasets should contain Indian legal questions, gold statutes/sections, gold cases, temporal as-of labels, and jurisdiction metadata.
