"""Pruebas críticas: aislamiento entre equipos, máquinas y códigos vecinos."""

from industrial_rag.config import Settings
from industrial_rag.diagnosis.generator import DiagnosticGenerator, ExtractiveFallbackClient
from industrial_rag.models import FaultTrigger
from industrial_rag.pipeline import TroubleshootingPipeline


def _pipeline() -> TroubleshootingPipeline:
    settings = Settings(
        use_memory_qdrant=True,
        equipment_registry_path="data/equipment_registry.json",
        sample_chunks_path="data/sample_chunks",
    )
    pipe = TroubleshootingPipeline(
        settings=settings,
        generator=DiagnosticGenerator(llm=ExtractiveFallbackClient(), settings=settings),
    )
    indexed = pipe.load_pilot_data()
    assert indexed >= 8
    return pipe


def test_vfd_e05_stays_on_danfoss_manual():
    pipe = _pipeline()
    report = pipe.troubleshoot(
        FaultTrigger(equipment_id="VFD-LINE1-02", query="Falla E-05")
    )
    assert report.unavailable is False
    assert report.pages
    assert min(report.pages) >= 114
    blob = report.raw_response.lower()
    assert "sobrecorriente" in blob or "aislamiento" in blob or "motor" in blob
    assert "tia portal" not in blob
    assert "s7-1500" not in blob


def test_plc_e05_stays_on_siemens_manual():
    pipe = _pipeline()
    report = pipe.troubleshoot(
        FaultTrigger(equipment_id="PLC-LINE1-01", query="Falla E-05")
    )
    assert report.unavailable is False
    blob = report.raw_response.lower()
    assert "módulo" in blob or "e/s" in blob or "24 vdc" in blob or "siemens" in blob
    assert "rampa" not in blob
    assert "fc-302" not in blob


def test_filter_never_returns_other_equipment_chunks():
    pipe = _pipeline()
    trigger = FaultTrigger(equipment_id="VFD-LINE1-02", query="E-05")
    filt = pipe.router.build_filter(trigger)
    chunks = pipe.searcher.search("E-05", filt, limit=10)
    assert chunks
    assert all(c.metadata.equipment_id == "VFD-LINE1-02" for c in chunks)
    assert all(c.metadata.manufacturer == "Danfoss" for c in chunks)
    assert all(c.metadata.machine_id == "PACK-LINE-01" for c in chunks)


def test_tube_machine_isolated_from_pack_line():
    pipe = _pipeline()
    report = pipe.troubleshoot(
        FaultTrigger(
            equipment_id="VFD-TUBE-01",
            machine_id="TUBE-FORMER-01",
            query="AL 38",
        )
    )
    assert report.unavailable is False
    assert report.machine_id == "TUBE-FORMER-01"
    blob = report.raw_response.lower()
    assert "sobretensión" in blob or "desaceleración" in blob or "frenado" in blob
    assert "linea_empaque" not in blob


def test_exact_fault_code_prefers_al38_over_al39():
    pipe = _pipeline()
    trigger = FaultTrigger(equipment_id="VFD-TUBE-01", query="AL 38")
    filt = pipe.router.build_filter(trigger)
    chunks = pipe.searcher.search("AL 38", filt, limit=3)
    assert chunks
    top = chunks[0]
    assert "AL 38" in top.metadata.fault_codes or "AL 38" in top.text.upper()
    assert "AL 39" not in top.metadata.fault_codes
