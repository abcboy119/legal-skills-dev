# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Wat dit project is

Een distributie van drie juridische AI-skills (prompts, geen runtime-code) die samen één 3-fase pijplijn vormen. De Python in `scripts/` en `tests/` bouwt of test de skills niet functioneel — hij **valideert en packaget** ze. De inhoud van de skills is Nederlandstalige Markdown met XML-achtige structuurtags.

```
documenten-audit (2.1.0) → ecli-verificatie (2.1.0) → audit-synthese (1.1.0)
   Claim Register            pure JSON (16 velden)      impactanalyse + actielijst
   + manifest-template       + bronbestanden
```

Documentatie-bron: `docs/workflow.md` (architectuur + waarom), `docs/conventions.md` (harde conventies), `docs/sync-checklist.md` (af te werken vóór elke release).

## Commando's

```bash
pip install -r requirements.txt                          # eenmalig (jsonschema)

python3 scripts/package_skills.py --validate-only        # frontmatter + structuur
python3 scripts/generate_manifests.py --check            # hashes references/assets
python3 tests/test_pipeline_contracts.py                 # integratietest (196 assertions)

python3 scripts/package_skills.py                        # bouw alle skills → dist/
python3 scripts/package_skills.py documenten-audit       # één skill
python3 scripts/generate_manifests.py                    # MANIFEST.json regenereren
```

Deze drie checks zijn ook exact de CI-pipeline (`.github/workflows/ci.yml`).

Eén test draaien: de testsuite is een handgeschreven runner met pytest-compatibele wrappers, dus
`python3 -m pytest tests/test_pipeline_contracts.py::test_34 -v` (nummers ↔ functies staan onderaan `tests/test_pipeline_contracts.py`). Zonder pytest: `python3 -c "import sys; sys.path.insert(0,'tests'); import test_pipeline_contracts as t; t.test_q9_case002_bulk_modus()"`.

> `check()` print `FAIL` maar raise't niets. De genummerde wrappers lopen daarom via `_run()`, dat de FAIL-teller vóór en na vergelijkt en er een echte assertie van maakt; de controlefuncties zelf staan op `__test__ = False` zodat pytest ze niet dubbel verzamelt. Voeg je een controlefunctie toe, geef haar dan ook een `test_NN`-wrapper — zonder wrapper draait ze alleen in de directe run.

## Architectuur: waar de koppelingen zitten

**De tests zijn contracttests over tekst, geen unittests over code.** Ze grepen op letterlijke strings in `SKILL.md` en de references (bijv. `"Geen herkenbaar Claim Register aangetroffen"`, `"Gerelateerde_Claims"`, `"BEVESTIGD + LAAG"`, de ECLI-regex). Herformuleren van een zin in een SKILL.md breekt daarom regelmatig een test — dat is bedoeld gedrag, geen fout in de test. Check bij een failure eerst welke assertie in `tests/test_pipeline_contracts.py` op die string leunt.

**Elke skill wordt los gepackaged.** `package_skills.py` zipt alleen de eigen skill-map. Cross-skill bestandsverwijzingen zijn daarom dode links; test 16 (K11) dwingt actief af dat Fase 2 en 3 *geen* pad naar `documenten-audit/references/...` bevatten en in plaats daarvan een inline regel hebben.

**`output.schema.json` bestaat twee keer, byte-identiek.** Origineel: `skills/ecli-verificatie/assets/`, kopie: `skills/audit-synthese/assets/` (zodat Fase 3 self-contained blijft). Test 35 vergelijkt de bytes. Wijzig altijd beide en regenereer het MANIFEST van `audit-synthese`.

**`references/MANIFEST.json`** bevat sha256-hashes van alle `references/` + `assets/`-bestanden. Het staat in git (bron van waarheid) maar in `IGNORED_FILES` van de packager, dus het gaat nooit mee de `.skill`-zip in. Elke wijziging aan references/assets vereist `generate_manifests.py`, anders faalt CI.

**De frontmatter-parser is handgeschreven** (`parse_frontmatter` in `scripts/package_skills.py`), geen YAML-library. Hij ondersteunt alleen: `key: waarde`, block-scalar `key: >` met ingesprongen vervolgregels, inline-lijst `[a, b]` en inline-map `{k: "v"}`. Meerregelige YAML-lijsten (`- item` op eigen regels) of nested maps worden **niet** geparsed — gebruik de bestaande vorm in de drie SKILL.md's als sjabloon.

**Fixtures zijn worked examples, geen mocks.** `tests/fixtures/case-001/` is het referentievoorbeeld (5 claims, incl. bewust ongeldige ECLI in C003 en `"N/A"` in C002/C005); `case-002/` dekt bulk-modus (meerdere claims op dezelfde ECLI). De expected-outputs zijn tegelijk documentatie voor gebruikers — zie de README's in die mappen.

## Regels bij het wijzigen van een skill

Volledige procedure: `docs/conventions.md` §7 + `docs/sync-checklist.md`. De niet-vanzelfsprekende punten:

- **`version` bumpen is verplicht**, ook bij references-wijzigingen: PATCH = verduidelijking, MINOR = nieuwe functionaliteit, MAJOR = breaking change in output-schema of stappenstructuur. Bij een MAJOR-bump ook de downstream-skill MINOR-bumpen.
- **`last_updated` naar vandaag** en nooit in de toekomst — validator én test 23 controleren dit tegen de systeemdatum.
- **`name` moet exact de mapnaam zijn**; `description` 30–500 tekens getrimd.
- **`<disclaimer>`-blok direct ná `</role>`** met de letterlijke tekst "concept ter beoordeling" — de validator faalt zonder.
- **ECLI-conventie: `"N/A"`, nooit `""`.** Dit geldt in het Claim Register-schema, de JSON-output en de action-classification-matrix tegelijk.
- **Ongeldige ECLI's mogen niet stil verdwijnen**: ze blijven in de output met `ecli_formaat_geldig: false` en `oordeel: NIET_CONTROLEERBAAR`.
- **JSON-veldnamen altijd `snake_case`, JSON-waarden in het Nederlands** (`"BEVESTIGD"`, niet `"CONFIRMED"`). Skill-content is Nederlands; technische scripts mogen Engels commentaar hebben.
- **`<step number="N">` opeenvolgend zonder gaten** — de sync-checklist controleert dit handmatig.
- Bestanden: UTF-8 zonder BOM, LF, afsluitende newline; Markdown `kebab-case.md`, Python `snake_case.py`.

## Scope

Alleen de 3-fase audit-pijplijn zit in deze repo. `woo-avg-toets` en `stop-slop` worden elders onderhouden en vallen buiten het pipeline-contract. Externe scripts (`ecli_lookup_V10.py`, ECLI-scanner) zijn optionele hulpmiddelen tússen de fases en horen niet bij de distributie — zie `docs/workflow.md` §6.

`dist/` is een build-artefact en staat in `.gitignore`.

## Agent skills

### Issue tracker

Issues leven in GitHub Issues van `abcboy119/legal-skills-dev`, via de `gh` CLI. Zie `docs/agents/issue-tracker.md`.

### Triage labels

De vijf canonieke rollen, labelnaam gelijk aan de rolnaam (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). Zie `docs/agents/triage-labels.md`.

### Domain docs

Single-context: één `CONTEXT.md` + `docs/adr/` in de repo-root. Zie `docs/agents/domain.md`.
