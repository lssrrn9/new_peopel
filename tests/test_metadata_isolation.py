"""Prueba crítica: E-05 del VFD no debe contaminarse con el PLC."""

from industrial_rag.config import Settings
from industrial_rag.diagnosis.generator import ExtractiveFallbackClient, DiagnosticGenerator
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
    assert indexed >= 5
    return pipe


def test_vfd_e05_stays_on_danfoss_manual():
    pipe = _pipeline()
    report = pipe.troubleshoot(
        FaultTrigger(equipment_id="VFD-LINE1-02", query="Falla E-05")
    )
    assert report.unavailable is False
    assert report.pages
    assert min(report.pages) >= 114
    # Debe hablar de sobrecorriente / motor, no de módulo de E/S Siemens
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
