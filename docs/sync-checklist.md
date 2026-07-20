# Sync-checklist — juridische skills

> Doorloop deze checklist vóór elke release of commit op `skills/`. Werkt deze af voor elke gewijzigde skill, en voer daarna de globale stappen onderaan uit.

## Per skill (na wijziging van `SKILL.md`, `references/` of `assets/`)

- [ ] **Frontmatter compleet**: `name`, `description`, `version`, `last_updated`, `author`, `license`, `jurisdiction`, `compatibility`, `source` — alle velden aanwezig en gevuld.
- [ ] **`name`** komt exact overeen met de mapnaam onder `skills/`.
- [ ] **`version`** voldoet aan semver (`MAJOR.MINOR.PATCH`); bij breaking changes in output-schema of stappenstructuur → MAJOR bump.
- [ ] **`last_updated`** is `YYYY-MM-DD` en ligt niet in de toekomst.
- [ ] **`description`** is 30–500 tekens (getrimd) en bevat zowel de trigger-zinnen als de korte doelomschrijving.
- [ ] **`source`** wijst naar het juiste docs-bestand (meestal `docs/workflow.md`).
- [ ] **`references/`** bevat geen lege mappen; elke reference wordt daadwerkelijk gelinkt vanuit `SKILL.md`.
- [ ] **`assets/`** idem — geen dode templates.
- [ ] Alle Markdown-links binnen de skill (in `SKILL.md` naar `references/` en `assets/`) wijzen naar bestaande bestanden.
- [ ] Stappennummering in `<step number="N">` is opeenvolgend zonder gaten of duplicaten.
- [ ] Geen hard-coded paden buiten de skill-map (alle paden relatief binnen de skill, of via placeholder zoals `pad/naar/...`).

## Globaal (na wijzigingen in meerdere skills)

- [ ] **Contract-controle Fase 1 → Fase 2**: velden die `ecli-verificatie` uitleest uit het Claim Register staan nog in `documenten-audit/references/claim-register-schema.md`.
- [ ] **Contract-controle Fase 2 → Fase 3**: velden die `audit-synthese` uitleest uit de JSON staan in `ecli-verificatie/references/json-output-schema.md` én in `ecli-verificatie/assets/output.schema.json`.
- [ ] **Schema-kopie synchroon**: bij elke wijziging aan `ecli-verificatie/assets/output.schema.json` óók de kopie `audit-synthese/assets/output.schema.json` bijwerken (byte-identiek; de testsuite dwingt dit af) en het MANIFEST van audit-synthese regenereren.
- [ ] **ECLI-afspraken consistent**: `"N/A"` (niet `""`) wordt gebruikt in Claim Register-schema, JSON-output-schema, én action-classification-matrix.
- [ ] **`docs/workflow.md`** bevat nog steeds de actuele beschrijving van de pipeline.
- [ ] **`docs/conventions.md`** weerspiegelt de werkelijke velden in frontmatter.
- [ ] **`README.md`** bevat de juiste skill-lijst en versienummers.
- [ ] **Validator draait schoon**: `python3 scripts/package_skills.py --validate-only` rapporteert 0 fouten.
- [ ] **Build draait schoon**: `python3 scripts/package_skills.py --clean` gevolgd door build levert `.skill`-bestanden in `dist/` voor alle skills.
- [ ] **Voorbeeld-JSON valideert** tegen `output.schema.json` (handmatig: `python3 -c "import jsonschema, json; jsonschema.validate(json.load(open('skills/ecli-verificatie/assets/json-output-example.json')), json.load(open('skills/ecli-verificatie/assets/output.schema.json')))"`).
- [ ] **`last_updated`** van alle gewijzigde skills bijgewerkt naar vandaag.
