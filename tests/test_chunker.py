from industrial_rag.ingestion.chunker import chunk_fault_table_markdown, split_plain_text
from industrial_rag.ingestion.fault_codes import extract_fault_codes
from industrial_rag.models import ChunkMetadata


BASE = ChunkMetadata(
    machine_id="TUBE-FORMER-01",
    equipment_id="VFD-TUBE-01",
    manufacturer="Danfoss",
    model="FC-302",
    line="Formado_Tubos",
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
    assert chunks[0].metadata.equipment_id == "VFD-TUBE-01"
    assert "E-05" in chunks[0].metadata.fault_codes


def test_plain_text_chunks_keep_metadata_and_codes():
    text = "Alarma AL 38: Sobretensión en bus DC.\n\n" + ("Procedimiento de verificación. " * 40)
    chunks = split_plain_text(text, metadata_base=BASE, chunk_size=400, chunk_overlap=40)
    assert len(chunks) >= 1
    assert all(c.metadata.page_number == 114 for c in chunks)
    assert all(c.metadata.machine_id == "TUBE-FORMER-01" for c in chunks)
    assert any("AL 38" in c.metadata.fault_codes for c in chunks)


def test_extract_fault_codes_distinguish_neighbors():
    codes = extract_fault_codes("Consultar AL 38 y no confundir con AL 39")
    assert "AL 38" in codes
    assert "AL 39" in codes
