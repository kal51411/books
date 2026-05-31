"""Legal dataset ingestion pipeline for Indian legal sources."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID

from backend.app.domain.legal import LegalChunk, LegalDocument, SourceType


@dataclass(frozen=True)
class IngestionSource:
    path: Path
    source_type: SourceType
    source_url: str | None = None
    metadata: dict = field(default_factory=dict)


class OCRExtractor:
    def extract_text(self, source: IngestionSource) -> str:
        if source.path.suffix.lower() in {".txt", ".md"}:
            return source.path.read_text(encoding="utf-8")
        return f"OCR placeholder for {source.path.name}; production uses Tesseract/PaddleOCR."


class MetadataExtractor:
    def extract(self, source: IngestionSource, text: str) -> LegalDocument:
        return LegalDocument(
            source_type=source.source_type,
            title=source.metadata.get("title", source.path.stem),
            text=" ".join(text.split()),
            source_url=source.source_url,
            act_name=source.metadata.get("act_name"),
            section=source.metadata.get("section"),
            court=source.metadata.get("court"),
            citation=source.metadata.get("citation"),
            year=source.metadata.get("year"),
            state=source.metadata.get("state"),
            effective_date=source.metadata.get("effective_date"),
            amendment_date=source.metadata.get("amendment_date"),
            repeal_status=source.metadata.get("repeal_status"),
            metadata=source.metadata,
        )


class SectionAwareChunker:
    def chunk(self, document: LegalDocument, *, max_chars: int = 1200) -> list[LegalChunk]:
        paragraphs = [part.strip() for part in document.text.split("\n") if part.strip()] or [document.text]
        chunks: list[LegalChunk] = []
        for index, paragraph in enumerate(paragraphs):
            for offset in range(0, len(paragraph), max_chars):
                chunks.append(
                    LegalChunk(
                        document_id=document.id,
                        chunk_index=len(chunks),
                        paragraph=index + 1,
                        section=document.section,
                        text=paragraph[offset : offset + max_chars],
                    )
                )
        return chunks


class HierarchicalChunker:
    def chunk(self, document: LegalDocument) -> list[LegalChunk]:
        root = LegalChunk(document_id=document.id, chunk_index=0, text=document.text[:1800])
        children = SectionAwareChunker().chunk(document, max_chars=700)
        return [root, *[child.model_copy(update={"parent_id": root.id}) for child in children]]


class SemanticChunker:
    def chunk(self, document: LegalDocument) -> list[LegalChunk]:
        sentences = document.text.replace(";", ".").split(".")
        chunks = []
        buffer = ""
        for sentence in sentences:
            if len(buffer) + len(sentence) > 900 and buffer:
                chunks.append(LegalChunk(document_id=document.id, chunk_index=len(chunks), text=buffer))
                buffer = ""
            buffer = f"{buffer}. {sentence}".strip(". ")
        if buffer:
            chunks.append(LegalChunk(document_id=document.id, chunk_index=len(chunks), text=buffer))
        return chunks


class EmbeddingIndexer:
    async def index(self, document: LegalDocument, chunks: list[LegalChunk]) -> dict[str, UUID | int]:
        return {"document_id": document.id, "chunks_indexed": len(chunks)}


class LegalIngestionPipeline:
    def __init__(self, chunker: SectionAwareChunker | HierarchicalChunker | SemanticChunker | None = None) -> None:
        self.ocr = OCRExtractor()
        self.metadata = MetadataExtractor()
        self.chunker = chunker or SectionAwareChunker()
        self.indexer = EmbeddingIndexer()

    async def ingest(self, source: IngestionSource) -> dict[str, UUID | int]:
        text = self.ocr.extract_text(source)
        document = self.metadata.extract(source, text)
        chunks = self.chunker.chunk(document)
        return await self.indexer.index(document, chunks)
