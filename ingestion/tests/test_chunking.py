from backend.app.domain.legal import LegalDocument, SourceType
from ingestion.nyayagpt_ingestion.pipeline import (
    HierarchicalChunker,
    SectionAwareChunker,
    SemanticChunker,
)


def test_chunking_strategies_produce_chunks():
    document = LegalDocument(source_type=SourceType.INDIA_CODE, title="Test Act", text="Section 1. Text. Section 2. More text.", section="1")

    assert SectionAwareChunker().chunk(document)
    assert HierarchicalChunker().chunk(document)
    assert SemanticChunker().chunk(document)
