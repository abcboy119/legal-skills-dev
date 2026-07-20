# Juridische Skills

Drie juridische AI-skills in canonieke skill-structuur, geschikt voor Claude Code, OpenCode en Claude Desktop. Samen vormen ze een 3-fase audit- en verificatiepijplijn.

## Skills in deze distributie

| Skill | Doel | Versie |
|---|---|---|
| documenten-audit | Audit en vergelijk juridische documenten; IRAC-scores; Claim Register | 2.0.0 |
| ecli-verificatie | Verifieer claims tegen rechterlijke uitspraken; pure JSON-output | 2.0.0 |
| audit-synthese | Vertaal verificatie-JSON naar impactanalyse en actielijst | 1.0.0 |

De drie skills vormen een pipeline: `documenten-audit` -> `ecli-verificatie` -> `audit-synthese`. Zie `docs/workflow.md` voor de volledige workflow.

> **Niet in deze distributie:** `woo-avg-toets` (v4.2.0) en `stop-slop` (v1.0.0) worden apart onderhouden in een eigen repository en zijn niet opgenomen in deze zip.

## Structuur

- `skills/<name>/` — bron (SKILL.md + references/ + assets/)
- `dist/` — build-artifacts (`.skill`-bestanden)
- `docs/` — `workflow.md`, `conventions.md`, `sync-checklist.md`
- `scripts/` — `package_skills.py`

## Builden

```bash
python3 scripts/package_skills.py                      # alle skills -> dist/
python3 scripts/package_skills.py documenten-audit      # enkele skill
python3 scripts/package_skills.py --validate-only       # alleen checken
python3 scripts/package_skills.py --clean               # dist/ leegmaken eerst
```

## Verificatie

Na wijzigingen: werk `docs/sync-checklist.md` af.
