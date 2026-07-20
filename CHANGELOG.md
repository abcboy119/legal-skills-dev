# Changelog

Alle wijzigingen tussen `pipeline_review.zip` (originele upload) en `pipeline_review_fixed3.zip`.

## v3 — Round 3 (K7-K13 + P1-P8)

### Toegevoegd — Kwaliteit & Robuustheid (K7-K13)

- **K7 — Context-budget-strategie voor Fase 2**: nieuwe reference `skills/ecli-verificatie/references/context-budget.md` met per-claim verificatie-venster, chunking-strategie bij context-overflow, volgorde van verificatie (HOOG→LAAG), bulk-modus voor meerdere claims per ECLI, en signalen dat budget wordt overschreden. SKILL.md `<verification_unit>` uitgebreid met verwijzing.
- **K8 — Conflict-resolutie raw vs normalized JSON**: `references/source-handling.md` uitgebreid met normalisatie-controle, "bij twijfel raw wint"-regel, procedure bij grote discrepantie, en een voorbeelden-tabel met 4 typische situaties.
- **K9 — Disclaimer-afdwinging**: `<disclaimer>`-blok toegevoegd direct na `</role>` in alle 3 SKILL.md's, met verplichte tekst "concept ter beoordeling". `package_skills.py` validator controleert hierop (`DISCLAIMER_MARKER`).
- **K10 — compatibility versie-bewust**: nieuw optioneel frontmatter-veld `compatibility_versions` (map: `{platform: "versie-range"}`) in alle 3 skills. Parser in `package_skills.py` uitgebreid om inline-YAML-maps te herkennen. Validator checkt dat het een dict is als aanwezig.
- **K11 — Prompt-injectieverdediging versterken**: nieuwe reference `skills/documenten-audit/references/prompt-injection-defense.md` met verdediging in diepte (4 lagen): instructie-classificatie, structuursyntax-bescherming (escape `</step>`, `</role>`, `---`, `## Stap`), input-classificatie voor wrappers, output-validatie. Alle 3 SKILL.md's verwijzen ernaar.
- **K12 — package_skills.py fragiele --skill check**: `iter_skills()` retourneert nu lege lijst bij niet-bestaande skill in plaats van een pad dat niet is_dir(); caller checkt expliciet op lege lijst. Geen IndexError meer.
- **K13 — .skill vs .skill-zips naam consistentie**: README al in orde sinds v2 (`.skill`); bevestigd.

### Toegevoegd — Polish (P1-P8)

- **P1 — conventions.md voluit**: uitgebreid met encoding (UTF-8 zonder BOM), line-endings (LF), bestandnaamconventies (kebab-case voor MD/JSON, snake_case voor Python), Markdown-stijl, JSON-stijl, taalkeuze (Nederlands voor content, snake_case voor JSON-velden), update-procedure (semver-bump regels), versie-tracking references, multi-jurisdictie, CI-checks.
- **P2 — workflow.md scope-sectie**: nieuwe sectie §4 "Scope van deze distributie" die duidelijk maakt dat `woo-avg-toets` en `stop-slop` niet in deze distributie zitten en hoe ze zich verhouden tot de pijplijn. Sectie §5 "Multi-jurisdictie" toegevoegd.
- **P3 — Worked example end-to-end**: `tests/fixtures/case-001/` uitgebreid met `expected_audit.md` (Fase 1 output), `expected_verification.json` (Fase 2 output, 5 claims), `expected_synthese.md` (Fase 3 output met impactanalyse en actielijst), `input/manifest.json`. README van case-001 omgevormd tot volledig worked-example-document met handmatige test-instructies.
- **P4 — Action-matrix gat BEVESTIGD + LAAG**: nieuwe rij in `action-classification.md` met actie "Herformuleer bewering ondanks steun (extractie was vaag)" en toelichting waarom. Prioriteringsvolgorde uitgebreid van 7 naar 8 items.
- **P5 — Manifest-template JSON Schema**: nieuw bestand `skills/documenten-audit/assets/manifest.schema.json` (draft 2020-12) met `propertyNames.pattern` die ECLI's valideert. `manifest-template.json` uitgebreid met tweede voorbeeld-entry.
- **P6 — last_updated CI-check**: `package_skills.py` validator checkt nu dat `last_updated` niet in de toekomst ligt (`date.fromisoformat()` + vergelijking met vandaag).
- **P7 — Versie-tracking references**: nieuw script `scripts/generate_manifests.py` dat per-skill `references/MANIFEST.json` genereert met SHA-256 hashes van alle bestanden in `references/` en `assets/`. Ondersteunt `--check` mode voor CI. `MANIFEST.json` toegevoegd aan `IGNORED_FILES` in `package_skills.py` zodat het niet in de `.skill`-zip terechtkomt. Alle 3 skills hebben nu een `MANIFEST.json`.
- **P8 — Multi-jurisdictie conflicthantering**: nieuwe reference `skills/documenten-audit/references/jurisdiction-hierarchy.md` met hiërarchie EHRM > EU > NL, ECLI-prefix-herkenning, 4 typen conflicten (direct, EVRM, voorrangsregel, niet-bindend), procedure per fase, speciale regels per jurisdictie (margin of appreciation, pilot-judgment, retroactieve werking), en 3 uitgewerkte voorbeelden.

### Tests uitgebreid

`tests/test_pipeline_contracts.py` uitgebreid van 11 test-functies (59 assertions) naar 25 test-functies (142 assertions). Nieuwe tests dekken alle K7-K13 en P1-P8 fixes.

```
$ python3 tests/test_pipeline_contracts.py
Resultaat: 142 PASS / 0 FAIL
```

### Nieuwe bestanden in v3

```
skills/documenten-audit/references/context-budget.md            (K7, eigenlijk in ecli-verificatie — zie hieronder)
skills/documenten-audit/references/prompt-injection-defense.md  (K11)
skills/documenten-audit/references/jurisdiction-hierarchy.md    (P8)
skills/documenten-audit/assets/manifest.schema.json             (P5)
skills/ecli-verificatie/references/context-budget.md            (K7)
skills/audit-synthese/references/MANIFEST.json                  (P7, auto-gegenereerd)
skills/documenten-audit/references/MANIFEST.json                 (P7, auto-gegenereerd)
skills/ecli-verificatie/references/MANIFEST.json                 (P7, auto-gegenereerd)
scripts/generate_manifests.py                                    (P7)
tests/fixtures/case-001/expected_audit.md                        (P3)
tests/fixtures/case-001/expected_synthese.md                     (P3)
tests/fixtures/case-001/input/manifest.json                      (P3)
```

## v2 — Round 2 (K3-K6 + ECLI-formaatboolean)

Zie v2-changelog hieronder. Samenvattend: K3 (IRAC-rubric 1-5 ankers), K4 (agentic-file-parsing voluit), K5 (ECLI-regex + ecli-format.md), K6 (integratietest met 59 assertions), bonus-fix `ecli_formaat_geldig` boolean.

## v1 — Round 1 (B1-B5 + K1 + K2)

Zie v1-changelog hieronder. Samenvattend: B1 (README eerlijk), B2 (extractie_zekerheid doorgifte), B3 (ECLI = "N/A"), B4 (source in REQUIRED_FIELDS), B5 (sync-checklist.md), K1 (self-repair 2-pass), K2 (JSON Schema draft 2020-12).
