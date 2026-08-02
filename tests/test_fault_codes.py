from industrial_rag.ingestion.fault_codes import extract_fault_codes, query_fault_codes


def test_extract_common_industrial_codes():
    text = "Ver AL 38, ERR-04, E-05 y Fault 12 en la tabla."
    codes = extract_fault_codes(text)
    assert "AL 38" in codes
    assert "ERR-04" in codes or "ERR 04" in codes or any(c.startswith("ERR") for c in codes)
    assert "E-05" in codes or "E05" in codes or any("05" in c for c in codes)


def test_query_fault_codes():
    assert query_fault_codes("Falla AL 38 en el VFD") == ["AL 38"]
