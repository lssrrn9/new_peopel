from industrial_rag.ingestion.chunker import chunk_fault_table_markdown, split_plain_text
from industrial_rag.models import ChunkMetadata


BASE = ChunkMetadata(
    equipment_id="VFD-LINE1-02",
    manufacturer="Danfoss",
    model="FC-302",
    line="Linea_Empaque",
    manual_version="v3.1",
    page_number=114,
)


def test_fault_table_preserves_code_cause_solution():
    table = """
| Código | Causa | Solución |
| --- | --- | --- |
| E-05 | Sobrecorriente | Verificar aislamiento del motor |
| E-07 | Sobretensión DC | Aumentar desaceleración |
"""
    chunks = chunk_fault_table_markdown(table, metadata_base=BASE)
    assert len(chunks) == 2
    assert "E-05" in chunks[0].text
    assert "Sobrecorriente" in chunks[0].text
    assert "Verificar aislamiento" in chunks[0].text
    assert chunks[0].metadata.section == "fault_codes"
    assert chunks[0].metadata.equipment_id == "VFD-LINE1-02"


def test_plain_text_chunks_keep_metadata():
    text = "A" * 900 + "\n\n" + "B" * 100
    chunks = split_plain_text(text, metadata_base=BASE, chunk_size=400, chunk_overlap=40)
    assert len(chunks) >= 2
    assert all(c.metadata.page_number == 114 for c in chunks)
