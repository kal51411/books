from evaluation.nyayagpt_eval.metrics import RetrievalJudgment, mrr, ndcg_at_k, recall_at_k


def test_retrieval_metrics():
    judgment = RetrievalJudgment(query_id="q1", relevant_ids={"a", "b"}, ranked_ids=["c", "a", "b"])

    assert recall_at_k(judgment, 2) == 0.5
    assert round(ndcg_at_k(judgment, 3), 3) > 0
    assert mrr([judgment]) == 0.5
