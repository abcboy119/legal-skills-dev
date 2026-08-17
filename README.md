# Juridische Skills

[![CI Status](https://github.com/abcboy119/legal-skills-dev/actions/workflows/ci.yml/badge.svg)](https://github.com/abcboy119/legal-skills-dev/actions/workflows/ci.yml)
[![Test Pass Rate](https://img.shields.io/badge/tests-186%2F186%20PASS-brightgreen)](#verificatie)
[![Last Updated](https://img.shields.io/badge/last%20updated-2026--07--23-blue)](#)

> **Laatste update:** 2026-07-23 — Zie [CHANGELOG.md](CHANGELOG.md) voor wijzigingsgeschiedenis.

Drie juridische AI-skills in canonieke skill-structuur, geschikt voor Claude Code, OpenCode en Claude Desktop. Samen vormen ze een 3-fase audit- en verificatiepijplijn.

## Skills in deze distributie

| Skill | Doel | Versie |
|---|---|---|
| documenten-audit | Audit en vergelijk juridische documenten; IRAC-scores; Claim Register | 2.1.1 |
| ecli-verificatie | Verifieer claims tegen rechterlijke uitspraken; pure JSON-output | 2.1.1 |
| audit-synthese | Vertaal verificatie-JSON naar impactanalyse en actielijst | 1.2.0 |

De drie skills vormen een pipeline: `documenten-audit` -> `ecli-verificatie` -> `audit-synthese`. Zie `docs/workflow.md` voor de volledige workflow.

> **Niet in deze distributie:** `woo-avg-toets` (v4.2.0) en `stop-slop` (v1.0.0) worden apart onderhouden in een eigen repository en zijn niet opgenomen in deze zip.

## Structuur

- `skills/<name>/` — bron (SKILL.md + references/ + assets/)
- `dist/` — build-artifacts (`.skill`-bestanden)
- `docs/` — `workflow.md`, `conventions.md`, `sync-checklist.md`
- `scripts/` — `package_skills.py` (validator + builder), `generate_manifests.py` (versie-tracking)
- `tests/` — `test_pipeline_contracts.py` (integratietest) + `fixtures/case-001/` (worked example) + `fixtures/case-002/` (bulk-modus)

## Builden

```bash
python3 scripts/package_skills.py                      # alle skills -> dist/
python3 scripts/package_skills.py documenten-audit      # enkele skill
python3 scripts/package_skills.py --validate-only       # alleen checken
python3 scripts/package_skills.py --clean               # dist/ leegmaken eerst
```

## Verificatie

**Eenmalige installatie:**
```bash
pip install -r requirements.txt    # jsonschema (nodig voor integratietests)
```

**Pre-commit hook (optioneel):**
```bash
cp .git/hooks/commit-msg.sample .git/hooks/commit-msg 2>/dev/null || true
# De pre-commit hook voor automatische validatie staat in .git/hooks/
```

Na wijzigingen: werk `docs/sync-checklist.md` af en draai:

```bash
python3 scripts/package_skills.py --validate-only       # frontmatter + structuur
python3 scripts/generate_manifests.py --check            # references/assets hashes
python3 tests/test_pipeline_contracts.py                 # integratietest
```

Voor het worked-example: zie `tests/fixtures/case-001/README.md` voor een end-to-end walkthrough met verwachte outputs voor alle 3 fases.

Zie `CHANGELOG.md` voor de volledige wijzigingsgeschiedenis.
