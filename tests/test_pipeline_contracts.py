#!/usr/bin/env python3
"""Integratietest voor de juridische audit-pijplijn (Fase 1 -> 2 -> 3).

Deze test draait GEEN live LLM-calls. In plaats daarvan verifieert hij de
**contracten** tussen de drie skills:

1. Fase 1 Claim Register-structuur komt overeen met wat Fase 2 verwacht.
2. Fase 2 verwachte JSON-output valideert tegen het JSON Schema
   (`skills/ecli-verificatie/assets/output.schema.json`).
3. ECLI-afhandeling is consistent: `"N/A"` (niet `""`).
4. extractie_zekerheid is aanwezig in elke entry (B2-fix).
5. Ongeldige ECLI-syntax komt niet stil door — toelichting vermeldt het.
6. Action-classification-matrix in Fase 3 dekt alle 5 oordelen × 3 zekerheden.

Draaien:
    python3 tests/test_pipeline_contracts.py
of:
    python3 -m pytest tests/ -v
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "skills/ecli-verificatie/assets/output.schema.json"
EXAMPLE_PATH = ROOT / "skills/ecli-verificatie/assets/json-output-example.json"
CASE_DIR = ROOT / "tests/fixtures/case-001"
EXPECTED_VERIFICATION = CASE_DIR / "expected_verification.json"

ECLI_REGEX = re.compile(r"^ECLI:[A-Z]{2}:[A-Z0-9]+:\d{4}:[A-Za-z0-9.]+$")
ALLOWED_OORDELEN = {"BEVESTIGD", "GEDEELTELIJK", "NIET_BEVESTIGD", "TEGENGESPROKEN", "NIET_CONTROLEERBAAR"}
ALLOWED_ZEKERHEID = {"HOOG", "MIDDEN", "LAAG"}
REQUIRED_FIELDS = [
    "claim_id", "doc_id", "ecli", "ecli_formaat_geldig", "extractie_zekerheid",
    "bron_aangeleverd", "bronbestand", "instantie", "datum", "rechtsgebied",
    "bewering_analyse", "oordeel", "vindplaats", "broncitaat",
    "relevante_broninhoud", "toelichting",
]

PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {detail}")


def load_json(path: Path) -> list | dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonschema():
    try:
        import jsonschema  # type: ignore
        return jsonschema
    except ImportError:
        return None


# ------------------------------------------------------------------
# Test 1: JSON Schema-bestand zelf is geldige JSON
# ------------------------------------------------------------------
def test_schema_loads() -> None:
    print("\n[1] JSON Schema-bestand is parseerbaar")
    try:
        schema = load_json(SCHEMA_PATH)
    except Exception as e:
        check("schema parsed", False, str(e))
        return
    check("schema parsed", isinstance(schema, dict))
    check("schema heeft $schema", schema.get("$schema", "").startswith("https://json-schema.org/"))
    check("schema type=array", schema.get("type") == "array")
    check("schema minItems=1", schema.get("minItems") == 1)
    required = schema.get("items", {}).get("required", [])
    check("schema required bevat extractie_zekerheid", "extractie_zekerheid" in required)
    check("schema required bevat ecli_formaat_geldig", "ecli_formaat_geldig" in required)
    check("schema required bevat alle 16 velden", len(required) == 16, f"got {len(required)}")


# ------------------------------------------------------------------
# Test 2: Voorbeeld-JSON (json-output-example.json) valideert
# ------------------------------------------------------------------
def test_example_validates() -> None:
    print("\n[2] Voorbeeld-JSON valideert tegen schema")
    jsonschema = load_jsonschema()
    if jsonschema is None:
        check("jsonschema lib beschikbaar", False, "pip install jsonschema")
        return
    check("jsonschema lib beschikbaar", True)
    schema = load_json(SCHEMA_PATH)
    example = load_json(EXAMPLE_PATH)
    try:
        jsonschema.validate(example, schema)
        check("example.json valideert", True)
    except jsonschema.ValidationError as e:
        check("example.json valideert", False, str(e.message))


# ------------------------------------------------------------------
# Test 3: Expected verification (case-001) valideert tegen schema
# ------------------------------------------------------------------
def test_expected_validates() -> None:
    print("\n[3] Case-001 expected_verification.json valideert tegen schema")
    jsonschema = load_jsonschema()
    if jsonschema is None:
        check("jsonschema lib beschikbaar", False)
        return
    schema = load_json(SCHEMA_PATH)
    expected = load_json(EXPECTED_VERIFICATION)
    try:
        jsonschema.validate(expected, schema)
        check("expected_verification valideert", True)
    except jsonschema.ValidationError as e:
        check("expected_verification valideert", False, str(e.message))


# ------------------------------------------------------------------
# Test 4: ECLI-afhandeling in expected output
# ------------------------------------------------------------------
def test_ecli_handling() -> None:
    print("\n[4] ECLI-afhandeling consistent in expected output")
    expected = load_json(EXPECTED_VERIFICATION)
    check("expected heeft 5 entries", len(expected) == 5, f"got {len(expected)}")

    # ECLI = "N/A" exact, geen "" (B3-fix)
    na_entries = [e for e in expected if e["ecli"] == "N/A"]
    empty_entries = [e for e in expected if e["ecli"] == ""]
    check("N/A entries: exact 2 (C002, C005)", len(na_entries) == 2, f"got {len(na_entries)}")
    check("geen lege-string ECLI's", len(empty_entries) == 0, f"got {len(empty_entries)}")

    # Ongeldige ECLI-syntax (C003) — moet nog steeds in output staan, niet stil gedropt
    c003 = next((e for e in expected if e["claim_id"] == "C003"), None)
    check("C003 aanwezig (niet gedropt)", c003 is not None)
    if c003:
        check("C003 ECLI is exact 'ECLI:NL:HR:23:1'", c003["ecli"] == "ECLI:NL:HR:23:1")
        check("C003 ECLI is ongeldig volgens regex", not ECLI_REGEX.match(c003["ecli"]))
        check("C003 ecli_formaat_geldig=false", c003.get("ecli_formaat_geldig") is False)
        check("C003 extractie_zekerheid=LAAG", c003["extractie_zekerheid"] == "LAAG")
        check("C003 oordeel=NIET_CONTROLEERBAAR", c003["oordeel"] == "NIET_CONTROLEERBAAR")
        check("C003 toelichting vermeldt formaatprobleem", "formaat" in c003["toelichting"].lower())

    # ecli_formaat_geldig consistentie over alle entries
    for e in expected:
        expected_valid = bool(ECLI_REGEX.match(e["ecli"]))
        actual_valid = e.get("ecli_formaat_geldig")
        check(
            f"{e['claim_id']} ecli_formaat_geldig consistent met regex",
            expected_valid == actual_valid,
            f"expected {expected_valid}, got {actual_valid}"
        )


# ------------------------------------------------------------------
# Test 5: extractie_zekerheid in elke entry (B2-fix)
# ------------------------------------------------------------------
def test_extractie_zekerheid_present() -> None:
    print("\n[5] extractie_zekerheid aanwezig in elke entry")
    expected = load_json(EXPECTED_VERIFICATION)
    for e in expected:
        check(f"{e['claim_id']} heeft extractie_zekerheid", "extractie_zekerheid" in e)
        if "extractie_zekerheid" in e:
            check(f"{e['claim_id']} zekerheid is geldig enum",
                  e["extractie_zekerheid"] in ALLOWED_ZEKERHEID,
                  f"got {e['extractie_zekerheid']}")


# ------------------------------------------------------------------
# Test 6: Action-classification-matrix dekt alle gevallen
# ------------------------------------------------------------------
def test_action_matrix_coverage() -> None:
    print("\n[6] Action-classification-matrix dekt alle oordeel × zekerheid combinaties")
    matrix_path = ROOT / "skills/audit-synthese/references/action-classification.md"
    text = matrix_path.read_text(encoding="utf-8")
    for oordeel in ALLOWED_OORDELEN:
        check(f"matrix noemt {oordeel}", oordeel in text)
    for zekerheid in ALLOWED_ZEKERHEID:
        check(f"matrix noemt {zekerheid}", zekerheid in text)
    check("matrix noemt 'N/A' (B3-consistency)", "N/A" in text)


# ------------------------------------------------------------------
# Test 7: IRAC-rubric heeft ankers voor 1 t/m 5 (K3-fix)
# ------------------------------------------------------------------
def test_irac_rubric_ankers() -> None:
    print("\n[7] IRAC-rubric heeft ankers voor scores 1 t/m 5")
    rubric = (ROOT / "skills/documenten-audit/references/irac-rubric.md").read_text(encoding="utf-8")
    for n in range(1, 6):
        check(f"anker **{n}** aanwezig", f"**{n}**" in rubric)


# ------------------------------------------------------------------
# Test 8: ECLI-regex in Fase 1 SKILL.md (K5-fix)
# ------------------------------------------------------------------
def test_ecli_regex_in_skill() -> None:
    print("\n[8] ECLI-regex aanwezig in Fase 1 SKILL.md en references")
    skill_md = (ROOT / "skills/documenten-audit/SKILL.md").read_text(encoding="utf-8")
    ecli_ref = (ROOT / "skills/documenten-audit/references/ecli-format.md").read_text(encoding="utf-8")
    schema_ref = (ROOT / "skills/documenten-audit/references/claim-register-schema.md").read_text(encoding="utf-8")

    regex_present = "ECLI:[A-Z]{2}:[A-Z0-9]+:\\d{4}:[A-Za-z0-9.]+" in skill_md
    check("regex in SKILL.md Stap 9", regex_present)
    check("ecli-format.md bestaat", len(ecli_ref) > 100)
    check("ecli-format.md bevat regex", "ECLI:[A-Z]{2}" in ecli_ref)
    check("claim-register-schema.md bevat regex", "ECLI:[A-Z]{2}" in schema_ref)
    check("claim-register-schema.md noemt Opmerking-kolom", "Opmerking" in schema_ref)


# ------------------------------------------------------------------
# Test 9: Claim-register-template heeft Opmerking-kolom
# ------------------------------------------------------------------
def test_claim_register_template() -> None:
    print("\n[9] Claim-register-template heeft Opmerking-kolom")
    template = (ROOT / "skills/documenten-audit/assets/claim-register-template.md").read_text(encoding="utf-8")
    check("template bevat Opmerking-kolom", "Opmerking" in template)
    check("template bevat voorbeeld LAAG + opmerking", "LAAG" in template and "formaat" in template.lower())


# ------------------------------------------------------------------
# Test 10: package_skills.py validator draait schoon
# ------------------------------------------------------------------
def test_validator_runs() -> None:
    print("\n[10] package_skills.py --validate-only draait schoon")
    import subprocess
    result = subprocess.run(
        ["python3", str(ROOT / "scripts/package_skills.py"), "--validate-only"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    check("exit code 0", result.returncode == 0, f"stderr: {result.stderr}")
    check("3/3 skills valid in output", "3/3 skills valid" in result.stdout, result.stdout)


# ------------------------------------------------------------------
# Test 11: Self-repair fallback-entry valideert tegen schema (K1-fix)
# ------------------------------------------------------------------
def test_self_repair_fallback() -> None:
    print("\n[11] Self-repair fallback-entry valideert tegen schema")
    jsonschema = load_jsonschema()
    if jsonschema is None:
        check("jsonschema lib beschikbaar", False)
        return
    schema = load_json(SCHEMA_PATH)
    fallback = [{
        "claim_id": "_error",
        "doc_id": "_error",
        "ecli": "N/A",
        "ecli_formaat_geldig": False,
        "extractie_zekerheid": "LAAG",
        "bron_aangeleverd": False,
        "bronbestand": "",
        "instantie": "",
        "datum": "",
        "rechtsgebied": "",
        "bewering_analyse": "self-repair-failed",
        "oordeel": "NIET_CONTROLEERBAAR",
        "vindplaats": "",
        "broncitaat": "",
        "relevante_broninhoud": "",
        "toelichting": "JSON-validatie faalde na 2 pogingen. Handmatige controle vereist."
    }]
    try:
        jsonschema.validate(fallback, schema)
        check("fallback-entry valideert tegen schema", True)
    except jsonschema.ValidationError as e:
        check("fallback-entry valideert tegen schema", False, str(e.message))


def main() -> int:
    print("=" * 70)
    print("Integratietest: juridische audit-pijplijn (Fase 1 -> 2 -> 3)")
    print("Fixture: tests/fixtures/case-001/")
    print("=" * 70)

    test_schema_loads()
    test_example_validates()
    test_expected_validates()
    test_ecli_handling()
    test_extractie_zekerheid_present()
    test_action_matrix_coverage()
    test_irac_rubric_ankers()
    test_ecli_regex_in_skill()
    test_claim_register_template()
    test_validator_runs()
    test_self_repair_fallback()

    print("\n" + "=" * 70)
    print(f"Resultaat: {PASS} PASS / {FAIL} FAIL")
    print("=" * 70)
    return 0 if FAIL == 0 else 1


# pytest-compatibele wrappers
def test_01(): test_schema_loads()
def test_02(): test_example_validates()
def test_03(): test_expected_validates()
def test_04(): test_ecli_handling()
def test_05(): test_extractie_zekerheid_present()
def test_06(): test_action_matrix_coverage()
def test_07(): test_irac_rubric_ankers()
def test_08(): test_ecli_regex_in_skill()
def test_09(): test_claim_register_template()
def test_10(): test_validator_runs()
def test_11(): test_self_repair_fallback()


if __name__ == "__main__":
    sys.exit(main())
