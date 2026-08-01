from pathlib import Path

from industrial_rag.models import FaultTrigger
from industrial_rag.retrieval.router import MetadataRouter


def test_build_filter_hard_equipment_id():
    router = MetadataRouter(Path("data/equipment_registry.json"))
    trigger = FaultTrigger(equipment_id="VFD-LINE1-02", query="Falla E-05")
    filt = router.build_filter(trigger)

    keys = {c["key"]: c["match"]["value"] for c in filt["must"]}
    assert keys["metadata.equipment_id"] == "VFD-LINE1-02"
    assert keys["metadata.manufacturer"] == "Danfoss"
    assert keys["metadata.model"] == "FC-302"


def test_unknown_equipment_raises():
    router = MetadataRouter(Path("data/equipment_registry.json"))
    try:
        router.resolve_equipment("NO-EXISTE")
        assert False, "expected KeyError"
    except KeyError as exc:
        assert "NO-EXISTE" in str(exc)
