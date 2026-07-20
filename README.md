# Juridische Skills

Vijf juridische AI-skills in canonieke skill-structuur, geschikt voor Claude Code, OpenCode en Claude Desktop.

## Skills

| Skill | Doel | Versie |
|---|---|---|
| documenten-audit | Audit en vergelijk juridische documenten; IRAC-scores; Claim Register | 2.0.0 |
| ecli-verificatie | Verifieer claims tegen rechterlijke uitspraken; pure JSON-output | 2.0.0 |
| audit-synthese | Vertaal verificatie-JSON naar impactanalyse en actielijst | 1.0.0 |
| woo-avg-toets | Toets Woo/AVG/Wpg/Wjsg-besluiten vanuit verzoeker | 4.2.0 |
| stop-slop | Verwijder AI-schrijfpatronen uit proza (Engels) | 1.0.0 |

De eerste drie vormen een pipeline: documenten-audit -> ecli-verificatie -> audit-synthese. Zie docs/workflow.md voor de volledige workflow.

## Structuur

- skills/<name>/ : bron (SKILL.md + references/ + assets/)
- dist/ : build-artifacts (.skill-zips)
- docs/ : workflow.md, conventions.md, sync-checklist.md
- scripts/ : package_skills.py + tests
- Chat/ : chat-historie (archief)

## Builden

- python3 scripts/package_skills.py (alle skills -> dist/)
- python3 scripts/package_skills.py documenten-audit (enkele skill)
- python3 scripts/package_skills.py --validate-only (alleen checken)
- python3 scripts/package_skills.py --clean (dist/ leegmaken eerst)

## Verificatie

Na wijzigingen: werk docs/sync-checklist.md af.
