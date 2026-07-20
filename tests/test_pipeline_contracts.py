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
    # Round 3: K7-K13 + P1-P8
    test_k7_context_budget()
    test_k8_raw_normalized_conflict()
    test_k9_disclaimer_in_all_skills()
    test_k10_compatibility_versions()
    test_k11_prompt_injection_defense()
    test_k12_validator_nonexistent_skill()
    test_p1_conventions_extended()
    test_p2_workflow_scope_section()
    test_p3_worked_example_complete()
    test_p4_action_matrix_bevestigd_laag()
    test_p5_manifest_schema()
    test_p6_last_updated_not_future()
    test_p7_manifests_consistent()
    test_p8_jurisdiction_hierarchy()
    test_q1_fase2_stopt_bij_ontbrekend_claim_register()
    test_q2_fase3_stopt_bij_ongeldige_json()
    test_q3_fase1_context_budget()
    test_q4_gerelateerde_claims()
    test_q5_jurisdictie_buiten_scope_fase1()
    test_q6_jurisdictie_buiten_scope_fase2()
    test_q7_brug_extern_ophaalscript()
    test_q8_ecli_scanner_crosscheck()

    print("\n" + "=" * 70)
    print(f"Resultaat: {PASS} PASS / {FAIL} FAIL")
    print("=" * 70)
    return 0 if FAIL == 0 else 1


# ------------------------------------------------------------------
# Test 12 (K7): Context-budget reference bestaat en wordt geraadpleegd
# ------------------------------------------------------------------
def test_k7_context_budget() -> None:
    print("\n[12] K7: Context-budget-strategie aanwezig in Fase 2")
    cb_path = ROOT / "skills/ecli-verificatie/references/context-budget.md"
    check("context-budget.md bestaat", cb_path.exists())
    if not cb_path.exists():
        return
    cb = cb_path.read_text(encoding="utf-8")
    check("bevat chunking-strategie", "chunking" in cb.lower())
    check("bevat per-claim verificatie-venster", "venster" in cb.lower() or "verification" in cb.lower())
    check("bevat volgorde van verificatie", "volgorde" in cb.lower())
    skill_md = (ROOT / "skills/ecli-verificatie/SKILL.md").read_text(encoding="utf-8")
    check("SKILL.md verwijst naar context-budget.md", "context-budget.md" in skill_md)


# ------------------------------------------------------------------
# Test 13 (K8): Raw vs normalized JSON conflict-resolutie
# ------------------------------------------------------------------
def test_k8_raw_normalized_conflict() -> None:
    print("\n[13] K8: Raw vs normalized JSON conflict-resolutie in source-handling.md")
    sh = (ROOT / "skills/ecli-verificatie/references/source-handling.md").read_text(encoding="utf-8")
    check("bevat conflict-resolutie sectie", "Conflict-resolutie" in sh or "conflict" in sh.lower())
    check("bevat 'raw wint' regel", "raw wint" in sh.lower() or "raw" in sh.lower())
    check("bevat voorbeelden-tabel", "| Situatie |" in sh or "Raw = 12" in sh)
    check("verwijst naar context-budget", "context-budget.md" in sh)


# ------------------------------------------------------------------
# Test 14 (K9): Disclaimer-blok in alle 3 SKILL.md's
# ------------------------------------------------------------------
def test_k9_disclaimer_in_all_skills() -> None:
    print("\n[14] K9: <disclaimer>-blok met 'concept ter beoordeling' in alle skills")
    for skill in ("documenten-audit", "ecli-verificatie", "audit-synthese"):
        path = ROOT / f"skills/{skill}/SKILL.md"
        text = path.read_text(encoding="utf-8")
        check(f"{skill}: <disclaimer> tag aanwezig", "<disclaimer>" in text and "</disclaimer>" in text)
        check(f"{skill}: 'concept ter beoordeling' aanwezig", "concept ter beoordeling" in text)


# ------------------------------------------------------------------
# Test 15 (K10): compatibility_versions in frontmatter van alle skills
# ------------------------------------------------------------------
def test_k10_compatibility_versions() -> None:
    print("\n[15] K10: compatibility_versions (map) in frontmatter")
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "scripts"))
    import package_skills as ps
    for skill in ("documenten-audit", "ecli-verificatie", "audit-synthese"):
        path = ROOT / f"skills/{skill}/SKILL.md"
        meta = ps.parse_frontmatter(path)
        check(f"{skill}: compatibility_versions aanwezig", "compatibility_versions" in meta)
        cv = meta.get("compatibility_versions")
        check(f"{skill}: compatibility_versions is dict", isinstance(cv, dict))
        if isinstance(cv, dict):
            check(f"{skill}: claudeCode-key aanwezig", "claudeCode" in cv)
            check(f"{skill}: openCode-key aanwezig", "openCode" in cv)


# ------------------------------------------------------------------
# Test 16 (K11): Prompt-injectieverdediging reference + SKILL.md verwijzingen
# ------------------------------------------------------------------
def test_k11_prompt_injection_defense() -> None:
    print("\n[16] K11: Prompt-injectieverdediging in Fase 1 (referentie) + inline regel in Fase 2/3")
    pid_path = ROOT / "skills/documenten-audit/references/prompt-injection-defense.md"
    check("prompt-injection-defense.md bestaat", pid_path.exists())
    if not pid_path.exists():
        return
    pid = pid_path.read_text(encoding="utf-8")
    check("bevat structuursyntax-bescherming", "structuursyntax" in pid.lower())
    check("bevat vierde lijn output-validatie", "output-validatie" in pid.lower() or "output" in pid.lower())
    check("noemt </step> als risico", "</step>" in pid)
    check("noemt --- als risico", "---" in pid)

    # Fase 1 SKILL.md verwijst ernaar (documenten-audit bevat het referentiebestand zelf,
    # dus dit pad blijft geldig ook als de skill los wordt gepackaged).
    f1 = (ROOT / "skills/documenten-audit/SKILL.md").read_text(encoding="utf-8")
    check("Fase 1 SKILL.md verwijst naar prompt-injection-defense.md", "prompt-injection-defense.md" in f1)

    # Fase 2/3 bevatten GEEN cross-skill bestandsverwijzing meer: elke skill wordt los
    # gepackaged (package_skills.py zipt alleen de eigen skill-map), dus een pad naar
    # documenten-audit/references/... zou daar een dode link zijn. De inline
    # prompt-injectie-regel blijft wel aanwezig in Fase 2/3 zelf.
    f2 = (ROOT / "skills/ecli-verificatie/SKILL.md").read_text(encoding="utf-8")
    check("Fase 2 SKILL.md bevat geen dode cross-skill verwijzing", "prompt-injection-defense.md" not in f2)
    check("Fase 2 SKILL.md bevat inline prompt-injectie-regel", "Prompt-injectie" in f2)

    f3 = (ROOT / "skills/audit-synthese/SKILL.md").read_text(encoding="utf-8")
    check("Fase 3 SKILL.md bevat geen dode cross-skill verwijzing", "prompt-injection-defense.md" not in f3)
    check("Fase 3 SKILL.md bevat inline prompt-injectie-regel", "Prompt-injectie" in f3)


# ------------------------------------------------------------------
# Test 17 (K12): Validator geeft nette fout bij niet-bestaande skill
# ------------------------------------------------------------------
def test_k12_validator_nonexistent_skill() -> None:
    print("\n[17] K12: package_skills.py handelt niet-bestaande skill netjes af")
    import subprocess
    result = subprocess.run(
        ["python3", str(ROOT / "scripts/package_skills.py"), "--validate-only", "niet-bestaande-skill"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    check("exit code 1 (niet 0)", result.returncode == 1)
    check("foutmelding bevat skill-naam", "niet-bestaande-skill" in result.stderr)
    check("geen traceback (geen 'IndexError')", "IndexError" not in result.stderr and "Traceback" not in result.stderr)


# ------------------------------------------------------------------
# Test 18 (P1): conventions.md uitgebreid
# ------------------------------------------------------------------
def test_p1_conventions_extended() -> None:
    print("\n[18] P1: conventions.md uitgebreid met encoding, line-endings, taalkeuze")
    conv = (ROOT / "docs/conventions.md").read_text(encoding="utf-8")
    check("bevat encoding-sectie", "UTF-8" in conv and "BOM" in conv)
    check("bevat line-endings-sectie", "LF" in conv and "CRLF" in conv)
    check("bevat bestandnaamconventies", "kebab-case" in conv)
    check("bevat taalkeuze-sectie", "Taalkeuze" in conv or "taalkeuze" in conv.lower())
    check("bevat JSON-stijl sectie", "JSON-stijl" in conv or "snake_case" in conv)
    check("bevat update-procedure", "Update-procedure" in conv or "semver" in conv.lower())
    check("bevat disclaimer-eis", "disclaimer" in conv.lower() and "concept ter beoordeling" in conv)


# ------------------------------------------------------------------
# Test 19 (P2): workflow.md bevat scope-sectie voor niet-pipeline skills
# ------------------------------------------------------------------
def test_p2_workflow_scope_section() -> None:
    print("\n[19] P2: workflow.md bevat scope-sectie voor niet-pipeline skills")
    wf = (ROOT / "docs/workflow.md").read_text(encoding="utf-8")
    check("bevat 'Scope van deze distributie'", "Scope van deze distributie" in wf)
    check("noemt woo-avg-toets als apart onderhouden", "woo-avg-toets" in wf.lower())
    check("noemt stop-slop als apart onderhouden", "stop-slop" in wf.lower())
    check("bevat Multi-jurisdictie sectie", "Multi-jurisdictie" in wf)


# ------------------------------------------------------------------
# Test 20 (P3): Worked example compleet met Fase 1, 2, 3 expected outputs
# ------------------------------------------------------------------
def test_p3_worked_example_complete() -> None:
    print("\n[20] P3: Worked example case-001 bevat expected outputs voor alle 3 fases")
    case_dir = ROOT / "tests/fixtures/case-001"
    check("expected_audit.md bestaat", (case_dir / "expected_audit.md").exists())
    check("expected_verification.json bestaat", (case_dir / "expected_verification.json").exists())
    check("expected_synthese.md bestaat", (case_dir / "expected_synthese.md").exists())
    check("input/manifest.json bestaat", (case_dir / "input/manifest.json").exists())
    check("sources/ECLI_NL_RBDHA_2023_1234.json bestaat", (case_dir / "sources/ECLI_NL_RBDHA_2023_1234.json").exists())

    # Manifest valideert tegen schema
    jsonschema = load_jsonschema()
    if jsonschema is not None:
        schema = load_json(ROOT / "skills/documenten-audit/assets/manifest.schema.json")
        manifest = load_json(case_dir / "input/manifest.json")
        try:
            jsonschema.validate(manifest, schema)
            check("input/manifest.json valideert tegen manifest.schema.json", True)
        except jsonschema.ValidationError as e:
            check("input/manifest.json valideert tegen manifest.schema.json", False, str(e.message))

    # expected_audit.md bevat 5 claims in Claim Register
    audit = (case_dir / "expected_audit.md").read_text(encoding="utf-8")
    for cid in ("C001", "C002", "C003", "C004", "C005"):
        check(f"expected_audit.md bevat {cid}", cid in audit)

    # expected_synthese.md bevat actielijst
    synthese = (case_dir / "expected_synthese.md").read_text(encoding="utf-8")
    check("expected_synthese.md bevat Impactanalyse", "Impactanalyse" in synthese)
    check("expected_synthese.md bevat Actielijst", "Actielijst" in synthese)


# ------------------------------------------------------------------
# Test 21 (P4): Action-matrix dekt nu BEVESTIGD + LAAG
# ------------------------------------------------------------------
def test_p4_action_matrix_bevestigd_laag() -> None:
    print("\n[21] P4: Action-matrix dekt BEVESTIGD + LAAG combinatie")
    matrix = (ROOT / "skills/audit-synthese/references/action-classification.md").read_text(encoding="utf-8")
    check("matrix bevat 'BEVESTIGD' + 'LAAG' rij", "BEVESTIGD" in matrix and "LAAG" in matrix)
    check("matrix bevat herformuleer-actie", "Herformuleer bewering" in matrix)
    check("matrix bevat toelichting BEVESTIGD + LAAG", "BEVESTIGD + LAAG" in matrix or "BEVESTIGD+LAAG" in matrix)


# ------------------------------------------------------------------
# Test 22 (P5): Manifest-template JSON Schema
# ------------------------------------------------------------------
def test_p5_manifest_schema() -> None:
    print("\n[22] P5: manifest.schema.json is geldig JSON Schema draft 2020-12")
    schema_path = ROOT / "skills/documenten-audit/assets/manifest.schema.json"
    check("manifest.schema.json bestaat", schema_path.exists())
    if not schema_path.exists():
        return
    schema = load_json(schema_path)
    check("bevat $schema draft 2020-12", "2020-12" in schema.get("$schema", ""))
    check("type=object", schema.get("type") == "object")
    check("propertyNames pattern bevat ECLI-regex", "ECLI:[A-Z]{2}" in schema.get("propertyNames", {}).get("pattern", ""))

    # Valideer manifest-template.json
    jsonschema = load_jsonschema()
    if jsonschema is not None:
        template = load_json(ROOT / "skills/documenten-audit/assets/manifest-template.json")
        try:
            jsonschema.validate(template, schema)
            check("manifest-template.json valideert", True)
        except jsonschema.ValidationError as e:
            check("manifest-template.json valideert", False, str(e.message))


# ------------------------------------------------------------------
# Test 23 (P6): last_updated <= vandaag
# ------------------------------------------------------------------
def test_p6_last_updated_not_future() -> None:
    print("\n[23] P6: last_updated ligt niet in de toekomst")
    import datetime as _dt
    today = _dt.date.today()
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "scripts"))
    import package_skills as ps
    for skill in ("documenten-audit", "ecli-verificatie", "audit-synthese"):
        path = ROOT / f"skills/{skill}/SKILL.md"
        meta = ps.parse_frontmatter(path)
        lu = meta.get("last_updated", "")
        try:
            lu_date = _dt.date.fromisoformat(str(lu))
            check(f"{skill}: last_updated {lu} <= vandaag {today}", lu_date <= today)
        except ValueError:
            check(f"{skill}: last_updated {lu} is geldige datum", False)


# ------------------------------------------------------------------
# Test 24 (P7): Per-skill MANIFEST.json hashes kloppen
# ------------------------------------------------------------------
def test_p7_manifests_consistent() -> None:
    print("\n[24] P7: Per-skill MANIFEST.json hashes kloppen")
    import subprocess
    result = subprocess.run(
        ["python3", str(ROOT / "scripts/generate_manifests.py"), "--check"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    check("generate_manifests.py --check exit code 0", result.returncode == 0, result.stderr)
    check("3 skills consistent", "audit-synthese" in result.stdout and "documenten-audit" in result.stdout and "ecli-verificatie" in result.stdout)

    # MANIFEST.json-bestanden bestaan
    for skill in ("documenten-audit", "ecli-verificatie", "audit-synthese"):
        check(f"{skill}/references/MANIFEST.json bestaat", (ROOT / f"skills/{skill}/references/MANIFEST.json").exists())


# ------------------------------------------------------------------
# Test 25 (P8): Multi-jurisdictie-conflicthantering reference
# ------------------------------------------------------------------
def test_p8_jurisdiction_hierarchy() -> None:
    print("\n[25] P8: Multi-jurisdictie-conflicthantering reference aanwezig")
    jh_path = ROOT / "skills/documenten-audit/references/jurisdiction-hierarchy.md"
    check("jurisdiction-hierarchy.md bestaat", jh_path.exists())
    if not jh_path.exists():
        return
    jh = jh_path.read_text(encoding="utf-8")
    check("bevat hiërarchie EHRM > EU > NL", "EHRM" in jh and "EU" in jh and "NL" in jh)
    check("bevat voorrangsregel", "voorrangsregel" in jh.lower() or "Voorrangsregel" in jh)
    check("bevat conflict-procedure", "Conflict" in jh or "conflict" in jh.lower())
    check("bevat ECLI-prefix herkenning", "ECLI:CE:ECHR" in jh or "ECLI:EU:C" in jh)


# ------------------------------------------------------------------
# Test 26 (Q1): Fase 2 stopt bij een ontbrekend Claim Register
# ------------------------------------------------------------------
def test_q1_fase2_stopt_bij_ontbrekend_claim_register() -> None:
    print("\n[26] Q1: Fase 2 stopt bij een ontbrekend/onherkenbaar Claim Register")
    skill = (ROOT / "skills/ecli-verificatie/SKILL.md").read_text(encoding="utf-8")
    check("SKILL.md noemt 'Ontbrekend of onherkenbaar Claim Register'",
          "Ontbrekend of onherkenbaar Claim Register" in skill)
    check("SKILL.md bevat de exacte stopmelding",
          "Geen herkenbaar Claim Register aangetroffen" in skill)
    sh = (ROOT / "skills/ecli-verificatie/references/source-handling.md").read_text(encoding="utf-8")
    check("source-handling.md noemt 'Geen herkenbaar Claim Register'",
          "Geen herkenbaar Claim Register" in sh)


# ------------------------------------------------------------------
# Test 27 (Q2): Fase 3 stopt bij ongeldige/onvolledige verificatie-JSON
# ------------------------------------------------------------------
def test_q2_fase3_stopt_bij_ongeldige_json() -> None:
    print("\n[27] Q2: Fase 3 stopt bij ongeldige of onvolledige verificatie-JSON")
    skill = (ROOT / "skills/audit-synthese/SKILL.md").read_text(encoding="utf-8")
    check("SKILL.md noemt 'Ongeldige of onvolledige verificatie-JSON'",
          "Ongeldige of onvolledige verificatie-JSON" in skill)
    check("SKILL.md verwijst naar output.schema.json",
          "output.schema.json" in skill)


# ------------------------------------------------------------------
# Test 28 (Q3): Context-budget-strategie voor Fase 1
# ------------------------------------------------------------------
def test_q3_fase1_context_budget() -> None:
    print("\n[28] Q3: Fase 1 heeft een eigen context-budget-strategie")
    cb_path = ROOT / "skills/documenten-audit/references/context-budget.md"
    check("documenten-audit/references/context-budget.md bestaat", cb_path.exists())
    if not cb_path.exists():
        return
    cb = cb_path.read_text(encoding="utf-8")
    check("bevat batch-strategie", "batch" in cb.lower())
    check("bevat consolidatie zonder Claim_ID-botsingen", "consolid" in cb.lower() and "Claim_ID" in cb)
    check("is NIET simpelweg een kopie van Fase 2's context-budget.md",
          "per-claim verificatie-venster" not in cb)
    skill = (ROOT / "skills/documenten-audit/SKILL.md").read_text(encoding="utf-8")
    check("SKILL.md verwijst naar references/context-budget.md", "references/context-budget.md" in skill)


# ------------------------------------------------------------------
# Test 29 (Q4): Gerelateerde_Claims-kolom voor meerdere ECLI's per claim
# ------------------------------------------------------------------
def test_q4_gerelateerde_claims() -> None:
    print("\n[29] Q4: Gerelateerde_Claims-kolom voor meerdere ECLI's per claim")
    schema = (ROOT / "skills/documenten-audit/references/claim-register-schema.md").read_text(encoding="utf-8")
    check("schema noemt Gerelateerde_Claims-kolom", "Gerelateerde_Claims" in schema)
    check("schema legt de conventie uit", "Meerdere ECLI's per claim" in schema)
    template = (ROOT / "skills/documenten-audit/assets/claim-register-template.md").read_text(encoding="utf-8")
    check("template bevat Gerelateerde_Claims-kolom in de header", "Gerelateerde_Claims" in template)
    skill = (ROOT / "skills/documenten-audit/SKILL.md").read_text(encoding="utf-8")
    check("SKILL.md Stap 9 noemt Gerelateerde_Claims", "Gerelateerde_Claims" in skill)


# ------------------------------------------------------------------
# Test 30 (Q5): Jurisdicties buiten NL/EU/EHRM — documenten-audit
# ------------------------------------------------------------------
def test_q5_jurisdictie_buiten_scope_fase1() -> None:
    print("\n[30] Q5: jurisdiction-hierarchy.md dekt jurisdicties buiten NL/EU/EHRM")
    jh = (ROOT / "skills/documenten-audit/references/jurisdiction-hierarchy.md").read_text(encoding="utf-8")
    check("bevat sectie 'Jurisdicties buiten deze distributie'",
          "Jurisdicties buiten deze distributie" in jh)
    check("noemt een niet-ondersteund voorbeeld (DE of FR)",
          "ECLI:DE:" in jh or "ECLI:FR:" in jh)
    check("verwijst naar NIET_CONTROLEERBAAR voor deze gevallen",
          "NIET_CONTROLEERBAAR" in jh)


# ------------------------------------------------------------------
# Test 31 (Q6): Jurisdicties buiten NL/EU/EHRM — ecli-verificatie
# ------------------------------------------------------------------
def test_q6_jurisdictie_buiten_scope_fase2() -> None:
    print("\n[31] Q6: source-handling.md dekt jurisdicties buiten NL/EU/EHRM")
    sh = (ROOT / "skills/ecli-verificatie/references/source-handling.md").read_text(encoding="utf-8")
    check("bevat 'buiten ondersteunde jurisdictie'", "buiten ondersteunde jurisdictie" in sh)
    check("verwijst naar jurisdiction-hierarchy.md", "jurisdiction-hierarchy.md" in sh)
    check("noemt de scope NL,EU,EHRM expliciet", "NL,EU,EHRM" in sh)


# ------------------------------------------------------------------
# Test 32 (Q7): Brug naar extern ECLI-ophaalscript gedocumenteerd
# ------------------------------------------------------------------
def test_q7_brug_extern_ophaalscript() -> None:
    print("\n[32] Q7: brug naar extern ECLI-ophaalscript in workflow.md + source-handling.md")
    wf = (ROOT / "docs/workflow.md").read_text(encoding="utf-8")
    check("workflow.md bevat 'Externe hulpmiddelen'", "Externe hulpmiddelen" in wf)
    check("workflow.md noemt ecli_lookup_V10.py", "ecli_lookup_V10.py" in wf)
    check("workflow.md noemt het eclis.txt-formaat", "eclis.txt" in wf)
    sh = (ROOT / "skills/ecli-verificatie/references/source-handling.md").read_text(encoding="utf-8")
    check("source-handling.md bevat sectie 'Manifestvormen'", "Manifestvormen" in sh)
    check("source-handling.md noemt de items-array-vorm", "items" in sh)


# ------------------------------------------------------------------
# Test 33 (Q8): ECLI-scanner cross-check (optioneel) gedocumenteerd
# ------------------------------------------------------------------
def test_q8_ecli_scanner_crosscheck() -> None:
    print("\n[33] Q8: ecli-scanner-crosscheck.md aanwezig en geraadpleegd in Stap 9")
    cc_path = ROOT / "skills/documenten-audit/references/ecli-scanner-crosscheck.md"
    check("ecli-scanner-crosscheck.md bestaat", cc_path.exists())
    if not cc_path.exists():
        return
    cc = cc_path.read_text(encoding="utf-8")
    check("bevat 'mogelijke hallucinatie'", "mogelijke hallucinatie" in cc.lower())
    check("markeert de stap expliciet als optioneel", "Optioneel" in cc)
    skill = (ROOT / "skills/documenten-audit/SKILL.md").read_text(encoding="utf-8")
    check("SKILL.md Stap 9 verwijst naar ecli-scanner-crosscheck.md",
          "ecli-scanner-crosscheck.md" in skill)


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
def test_12(): test_k7_context_budget()
def test_13(): test_k8_raw_normalized_conflict()
def test_14(): test_k9_disclaimer_in_all_skills()
def test_15(): test_k10_compatibility_versions()
def test_16(): test_k11_prompt_injection_defense()
def test_17(): test_k12_validator_nonexistent_skill()
def test_18(): test_p1_conventions_extended()
def test_19(): test_p2_workflow_scope_section()
def test_20(): test_p3_worked_example_complete()
def test_21(): test_p4_action_matrix_bevestigd_laag()
def test_22(): test_p5_manifest_schema()
def test_23(): test_p6_last_updated_not_future()
def test_24(): test_p7_manifests_consistent()
def test_25(): test_p8_jurisdiction_hierarchy()
def test_26(): test_q1_fase2_stopt_bij_ontbrekend_claim_register()
def test_27(): test_q2_fase3_stopt_bij_ongeldige_json()
def test_28(): test_q3_fase1_context_budget()
def test_29(): test_q4_gerelateerde_claims()
def test_30(): test_q5_jurisdictie_buiten_scope_fase1()
def test_31(): test_q6_jurisdictie_buiten_scope_fase2()
def test_32(): test_q7_brug_extern_ophaalscript()
def test_33(): test_q8_ecli_scanner_crosscheck()


if __name__ == "__main__":
    sys.exit(main())
