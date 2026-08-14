# Changelog

Wijzigingsgeschiedenis van de pijplijn. Oudste rondes onderaan (v1-v3 stammen uit de fase tussen `pipeline_review.zip` en `pipeline_review_fixed3.zip`).

## v2.1.1 / 1.2.0 — Consistentieronde: contractgaten en testbetrouwbaarheid

Versies: documenten-audit 2.1.1, ecli-verificatie 2.1.1, audit-synthese 1.2.0.

### Gecorrigeerde fouten

- **Testsuite gaf onder pytest vals groen**: `check()` telt en print een FAIL maar raist niet, en de `test_NN`-wrappers assertten niets. Daardoor rapporteerde de in de docstring gedocumenteerde route `python3 -m pytest tests/ -v` altijd succes, ook bij gefaalde controles. Wrappers lopen nu via `_run()`, dat de FAIL-teller vóór en na vergelijkt. Bijkomend: de controlefuncties heten zelf `test_*` en werden door pytest een tweede keer los verzameld (70 tests voor 35 controles); `__test__ = False` voorkomt dat. De directe route (`python3 tests/test_pipeline_contracts.py`) en de CI waren niet geraakt.
- **Stap 10 kon een manifest opleveren dat zijn eigen schema schendt**: de stap vroeg om "alle unieke ECLI's uit Stap 9", terwijl `assets/manifest.schema.json` via `propertyNames` alleen geldige ECLI's als sleutel toestaat en Stap 9 juist `N/A` en formaatfouten bewaart. Stap 10 benoemt de uitsluiting nu expliciet, inclusief de eis om weggelaten ECLI's onder het codeblok te vermelden.
- **`Gerelateerde_Claims` was een doodlopend contract**: `claim-register-schema.md` wees het signaleren van tegenstrijdige oordelen binnen een claimgroep toe aan Fase 3, maar `audit-synthese` noemde de kolom nergens. Fase 3 heeft nu een expliciete regel plus een beslistabel in `action-classification.md` (MINOR-bump).
- **Impact-rubric was intern tegenstrijdig en niet dekkend**: de categorie "Oordeel blijft overeind, alle claims bevestigd" eiste tegelijk 0 TEGENGESPROKEN én dat "alle TEGENGESPROKEN-claims bijzaak zijn", stond ondertussen wel een niet-bevestigde claim toe, en liet het geval "tegengesproken bijzaak-claim" ongedekt. Vervangen door vijf regels met dwingende volgorde; de vier fixture-rijen behouden hun bestaande classificatie.
- **`source-handling.md` noemde twee verschillende bronnen "primair"**: de koppelingshiërarchie wees normalized JSON aan, de conflict-resolutie raw XML. Nu onderscheiden als werkvoorkeur (normalized) versus gezag bij afwijking (raw).
- **`ecli-format.md` noemde `EU` en `CE` ISO 3166-1 alpha-2 landcodes**: dat zijn geen landen maar gereserveerde codes voor het HvJ EU respectievelijk het EHRM. Herschreven, met verwijzing naar de ondersteunde scope.
- **Spelfout** `voorangsregel` → `voorrangsregel` (2×, `jurisdiction-hierarchy.md`).
- **`tests/fixtures/case-001/README.md`**: `input/manifest.json` werd "Fase 1 output" genoemd terwijl het één ECLI bevat en het Stap 10-manifest in `expected_audit.md` er twee heeft — geherlabeld als subset van daadwerkelijk aangeleverde bronnen. Verouderde telling "Action-matrix 7 rijen" verwijderd (de matrix telt er 9).

### Testdekking

- Nieuwe `test_consistentieronde_contracten` (test 36) legt de twee gedragswijzigingen vast: de Stap 10-uitsluiting en de verwerking van `Gerelateerde_Claims` in Fase 3, plus de herschreven impact-rubric en de raw/normalized-formulering. Suite: 36 testfuncties / 196 assertions, alles groen.

### Bekend en niet gewijzigd

- De vorige regel meldde "34 testfuncties / 184 assertions"; feitelijk zijn het er sinds de sync-guard-commit 35 en 186. Historische regels zijn niet met terugwerkende kracht aangepast.

## v2.1.0 / 1.1.0 — Functionele-gaten-ronde (Q1-Q9) + housekeeping

Versies: documenten-audit 2.1.0, ecli-verificatie 2.1.0, audit-synthese 1.1.0. Ontwerp: `docs/superpowers/specs/2026-07-20-functionele-gaten-audit-pijplijn-design.md`.

### Functionele gaten gedicht (Q1-Q9)

- **Q1/Q2 — Fail-fast in Fase 2 en 3**: Fase 2 stopt bij een ontbrekend of onherkenbaar Claim Register; Fase 3 stopt bij ongeldige of onvolledige verificatie-JSON (16-velden-check tegen `assets/output.schema.json`).
- **Q3 — Context-budget-strategie voor Fase 1**: batch-strategie bij >~8 documenten of zeer lange documenten (`skills/documenten-audit/references/context-budget.md`).
- **Q4 — Meerdere ECLI's per claim**: splitsen over meerdere rijen met koppeling via `Gerelateerde_Claims` (`references/claim-register-schema.md`).
- **Q5/Q6 — Jurisdicties buiten NL/EU/EHRM**: expliciete afhandeling in beide skills in plaats van stilzwijgend overslaan.
- **Q7 — Brug naar extern ECLI-ophaalscript**: gedocumenteerde aansluiting op `ecli_lookup_V10.py` (extern onderhouden toolkit).
- **Q8 — ECLI-scanner cross-check**: optionele hallucinatie-detectie in Fase 1 (`references/ecli-scanner-crosscheck.md`).
- **Q9 — Bulk-modus testdekking**: nieuwe fixture `tests/fixtures/case-002/` (meerdere claims per ECLI).

### Housekeeping (clarity-audit)

- `requirements.txt` toegevoegd (`jsonschema`) — de testsuite importeerde het zonder dat het ergens gedeclareerd stond.
- `audit-synthese` is nu self-contained: eigen kopie van `assets/output.schema.json` in plaats van een verwijzing naar de sibling-skill (die niet mee-gepackaged werd).
- `PUSH_INSTRUCTIONS.md` ontdaan van gehardcodeerde commit-hashes/tag-claims die niet meer klopten.
- Stappenindex toegevoegd bovenaan de instructies van `documenten-audit/SKILL.md` (10 stappen in één oogopslag).
- Testsuite gegroeid naar 34 testfuncties / 184 assertions (alles groen).

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
