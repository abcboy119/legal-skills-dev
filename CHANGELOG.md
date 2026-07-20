# Changelog

Alle wijzigingen tussen `pipeline_review.zip` (originele upload) en `pipeline_review_fixed2.zip`.

## v2 — Round 2 (K3-K6 + ECLI-formaatboolean)

### Toegevoegd

- **K3 — IRAC-rubric aangevuld**: ankers voor scores 2 en 4, plus een score-matrix per IRAC-onderdeel (Issue, Rule, Application, Conclusion). `skills/documenten-audit/references/irac-rubric.md`.
- **K4 — Agentic File Parsing voluitgewerkt**: natuurlijke documentgrenzen (briefkop, datumregel, documenttype-wisseling, pagina-eindes), procedure bij geen delimiters, bijlagen/multi-file, edge-cases, en verplichte rapportage in Stap 1. `skills/documenten-audit/references/agentic-file-parsing.md`.
- **K5 — ECLI-regex in Fase 1**: nieuwe referentie `skills/documenten-audit/references/ecli-format.md` met formele syntaxis, voorbeelden van geldige/ongeldige ECLI's, en afhandelingsregels per fase. `claim-register-schema.md` uitgebreid met regex + nieuwe optionele kolom `Opmerking`. `SKILL.md` Stap 9 bevat nu de verplichte format-check.
- **K6 — Integratietest**: `tests/test_pipeline_contracts.py` met 59 assertions over schema, voorbeelden, ECLI-afhandeling, action-matrix, IRAC-ankers, validator, en self-repair fallback. Inclusief mini-casus `tests/fixtures/case-001/` met 2 input-documenten, 1 bronbestand, en verwachte verificatie-JSON.
- **Nieuw verplicht veld `ecli_formaat_geldig`** (boolean) in JSON-output Fase 2 — lost de spanning op tussen strenge schema-validatie (K2) en traceerbaarheid van ongeldige ECLI's (K5/B5). Ongeldige ECLI's worden niet meer stil gedropt; ze komen in `ecli` te staan met `ecli_formaat_geldig: false`.
- **Action-classification-matrix uitgebreid** met de `ecli_formaat_geldig`-dimensie en een expliciete prioriteringsvolgorde (Hoog/Midden/Laat).

### Gewijzigd

- `skills/ecli-verificatie/assets/output.schema.json` — `ecli`-pattern losser gemaakt (vrije string); nieuw verplicht veld `ecli_formaat_geldig`; `required`-lijst van 15 → 16 velden.
- `skills/ecli-verificatie/references/json-output-schema.md` — kolom `ecli_formaat_geldig` toegevoegd; conventies en self-repair Pass 2 bijgewerkt; fallback-entry bevat het nieuwe veld.
- `skills/ecli-verificatie/assets/json-output-example.json` — beide entries hebben `ecli_formaat_geldig`.
- `skills/documenten-audit/assets/claim-register-template.md` — `Opmerking`-kolom toegevoegd met voorbeeld.

### Tests

```
$ python3 tests/test_pipeline_contracts.py
Resultaat: 59 PASS / 0 FAIL
```

## v1 — Round 1 (B1-B5 + K1 + K2)

Zie `docs/sync-checklist.md` en eerdere commit. Samenvattend:

- **B1**: README eerlijk over 3 vs 5 skills.
- **B2**: `extractie_zekerheid` toegevoegd aan JSON-output — Fase 3 nu self-contained.
- **B3**: ECLI = `"N/A"` gestandaardiseerd (geen `""`).
- **B4**: `source` toegevoegd aan `REQUIRED_FIELDS` in `package_skills.py`.
- **B5**: `docs/sync-checklist.md` aangemaakt.
- **K1**: Self-repair omgevormd tot 2-pass procedure (syntactisch + semantisch) met fallback-entry.
- **K2**: Echt JSON Schema draft 2020-12: `assets/output.schema.json`.

## Nog open (niet in deze release)

K7-K13 (context-budget, raw-vs-normalized conflict, disclaimer-afdwinging, compatibility-versies, prompt-injectie-versterking, package_skills.py fragility, `.skill` vs `.skill-zips`), P1-P8 (polish).
