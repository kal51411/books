"""Evaluation metrics for retrieval, generation, and legal accuracy."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalJudgment:
    query_id: str
    relevant_ids: set[str]
    ranked_ids: list[str]


def recall_at_k(judgment: RetrievalJudgment, k: int) -> float:
    if not judgment.relevant_ids:
        return 0.0
    return len(set(judgment.ranked_ids[:k]) & judgment.relevant_ids) / len(judgment.relevant_ids)


def mrr(judgments: list[RetrievalJudgment]) -> float:
    scores = []
    for judgment in judgments:
        rank = next((i + 1 for i, doc_id in enumerate(judgment.ranked_ids) if doc_id in judgment.relevant_ids), None)
        scores.append(0.0 if rank is None else 1 / rank)
    return sum(scores) / len(scores) if scores else 0.0


def ndcg_at_k(judgment: RetrievalJudgment, k: int) -> float:
    dcg = sum(
        (1 if doc_id in judgment.relevant_ids else 0) / math.log2(index + 2)
        for index, doc_id in enumerate(judgment.ranked_ids[:k])
    )
    ideal_hits = min(len(judgment.relevant_ids), k)
    ideal = sum(1 / math.log2(index + 2) for index in range(ideal_hits))
    return dcg / ideal if ideal else 0.0


def hallucination_rate(total_claims: int, unsupported_claims: int) -> float:
    return unsupported_claims / total_claims if total_claims else 0.0


def citation_correctness(valid_citations: int, total_citations: int) -> float:
    return valid_citations / total_citations if total_citations else 0.0
