from industrial_rag.diagnosis.prompts import SYSTEM_PROMPT, build_user_prompt
from industrial_rag.models import ChunkMetadata, RetrievedChunk


def test_prompt_requires_manual_only_and_page_reference():
    assert "ÚNICAMENTE" in SYSTEM_PROMPT or "unicamente" in SYSTEM_PROMPT.lower()
    assert "Información no disponible en el manual oficial" in SYSTEM_PROMPT

    chunk = RetrievedChunk(
        text="Falla E-05: Sobrecorriente",
        metadata=ChunkMetadata(
            equipment_id="VFD-LINE1-02",
            manufacturer="Danfoss",
            model="FC-302",
            line="Linea_Empaque",
            manual_version="v3.1",
            page_number=114,
            section="fault_codes",
        ),
        score=0.9,
    )
    prompt = build_user_prompt("VFD-LINE1-02", "E-05", [chunk])
    assert "VFD-LINE1-02" in prompt
    assert "página 114" in prompt
    assert "Pruebas de Campo" in prompt
    assert "Referencia del Manual" in prompt
