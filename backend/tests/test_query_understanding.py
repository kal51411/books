from backend.app.rag.query_understanding import QueryUnderstandingService


def test_arrest_query_identifies_criminal_law_and_bnss():
    result = QueryUnderstandingService().understand("Can police arrest without warrant?")

    assert "criminal_procedure" in result.legal_intents
    assert "Bharatiya Nagarik Suraksha Sanhita, 2023" in result.acts
