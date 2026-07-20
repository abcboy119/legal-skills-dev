# Definitieve Workflow: Juridische Documenten Audit & Verificatie Pipeline

## 1. Uitleg en Onderbouwing (Het "Waarom")

Deze workflow is ontworpen om juridische documenten te analyseren, de daarin gemaakte beweringen (gekoppeld aan ECLI's) objectief te verifiëren, en de resultaten vertaalbaar te maken naar een actiegericht advies. 

Deze pipeline lost vijf belangrijke knelpunten op:

1.  **Handoff-ruis (Van Audit naar Verificatie):** 
    *   *Probleem:* De audit-AI moest zelf beweringen uit de tekst distilleren, wat leidde tot missers en vage koppelingen.
    *   *Oplossing:* Skill 1 (`documenten-audit`) genereert nu een gestructureerd **Claim Register** (Stap 9) en een **Manifest Template** (Stap 10). Skill 2 hoeft deze alleen nog maar uit te lezen. Dit garandeert een feilloze overdracht.
2.  **Schending van de "Pure JSON" regel:** 
    *   *Probleem:* Een JSON-output die gevolgd wordt door tekstuitleg is slecht voor automatische parsing.
    *   *Oplossing:* De JSON-output in Skill 2 is absoluut de laatste output. De mensgerichte samenvatting en advies zijn ondergebracht in een aparte skill: Skill 3 (`audit-synthese`).
3.  **Reverse Traceerbaarheid & Blinde Vlekken:** 
    *   *Oplossing:* De JSON in Skill 2 bevat `claim_id` en `doc_id`. Bovendien registreert Skill 1 nu óók krachtige beweringen die *geen* ECLI hebben, zodat ze in de verificatie als `NIET_CONTROLEERBAAR` worden gemarkeerd in plaats van stilletjes te verdwijnen.
4.  **Extractie-Zekerheid & IRAC-Validatie:** 
    *   *Oplossing:* In Skill 1 wordt de juridische redenering strikt getoetst aan IRAC/CRAC-principes en krijgt elke geëxtraheerde claim een zelf ingeschatte zekerheidsscore (HOOG/MIDDEN/LAAG). Skill 2 gebruikt deze score om scherper te verifieren.
5.  **Robuuste JSON Generatie:** 
    *   *Oplossing:* Skill 2 bevat een verplicht self-repair mechanisme om parser-fouties in downstream applicaties te voorkomen.

### De Workflow in 3 Fases:
1.  **Fase 1 - Audit:** Analyseer documenten, ken IRAC-scores toe, en bereid een atomair Claim Register voor. *(Skill: documenten-audit)*
2.  **Fase 2 - Verificatie:** Koppel claims objectief aan rechterlijke uitspraken (XML/JSON) en output pure JSON. *(Skill: ecli-verificatie)*
3.  **Fase 3 - Synthese:** Vertaal de JSON-resultaten naar een impactanalyse en actielijst voor de juridische eindredacteur. *(Skill: audit-synthese)*

---

## 2. Architectuur & Modulaire Structuur

Elke skill is volledig zelfstandig (canonieke Anthropic structuur) opgebouwd:
- `SKILL.md`: De hoofdprompt met rollen, regels en stappen.
- `references/`: Zware schema's en definities (Progressive Disclosure).
- `assets/`: Statische templates voor de AI om te kopiëren.

### Fase 1: documenten-audit
- `SKILL.md` (10 stappen, van documentoverzicht tot manifest generatie)
- `references/irac-rubric.md` (Ankers voor kwaliteitsscore 1/3/5)
- `references/claim-register-schema.md` (Kolomdefinities, Extractie_Zekerheid, Gerelateerde_Claims)
- `references/agentic-file-parsing.md` (Hoe meerdere docs te scheiden)
- `references/ecli-format.md` (Geldige/ongeldige ECLI-voorbeelden bij de regex-check)
- `references/context-budget.md` (Batch-strategie bij veel of lange documenten)
- `references/prompt-injection-defense.md` (Verdediging in diepte, 4 lagen)
- `references/jurisdiction-hierarchy.md` (EHRM > EU > NL, conflictregels)
- `references/ecli-scanner-crosscheck.md` (Optionele cross-check tegen scanner-output)
- `assets/manifest-template.json` (JSON template voor Fase 2 input)
- `assets/manifest.schema.json` (JSON Schema voor het manifest-template)
- `assets/claim-register-template.md` (Markdown template voor output)

### Fase 2: ecli-verificatie
- `SKILL.md` (4 stappen, streng naar pure JSON)
- `references/source-handling.md` (Manifest, raw vs normalized JSON, N/A afhandeling)
- `references/judgment-definitions.md` (De 5 oordelen met voorbeelden)
- `references/json-output-schema.md` (Velden, self-repair procedure, harde stop-regel)
- `references/context-budget.md` (Per-claim venster, chunking, bulk-modus)
- `assets/output.schema.json` (JSON Schema draft 2020-12, de 16 verplichte velden)
- `assets/json-output-example.json` (Voorbeeld van verwachte output)

### Fase 3: audit-synthese
- `SKILL.md` (3 stappen, impactanalyse naar actielijst)
- `references/impact-analysis-rubric.md` (Classificatie van "Gecorrigeerde impact")
- `references/action-classification.md` (Matrix: Oordeel + Extractie_Zekerheid -> Actie)
- `assets/action-list-template.md` (Template voor de eindredacteur)
- `assets/output.schema.json` (Kopie van het Fase 2-schema voor de 16-velden-check; wordt byte-identiek gehouden — zie sync-checklist)

Daarnaast bevat elke skill een auto-gegenereerd `references/MANIFEST.json` (sha256-hashes, zie `docs/conventions.md` §8); dat bestand wordt niet mee-gepackaged.

---

## 3. Gedeelde Conventies
Zie `docs/conventions.md` voor de gestandaardiseerde YAML-frontmatter (zoals `jurisdiction`, `version`, `compatibility_versions`), disclaimer-tekst, JSON-escaping regels, encoding- en bestandnaamconventies, taalkeuze, en update-procedure.

---

## 4. Scope van deze distributie

Deze distributie bevat uitsluitend de 3-fase audit-pijplijn (`documenten-audit` → `ecli-verificatie` → `audit-synthese`). Andere juridische skills die in het bredere ecosysteem bestaan — `woo-avg-toets` (v4.2.0, toetsen van Woo/AVG/Wpg/Wjsg-besluiten vanuit verzoeker) en `stop-slop` (v1.0.0, verwijderen van AI-schrijfpatronen uit proza) — worden apart onderhouden en vallen **niet** onder het pipeline-contract van deze workflow.

De vijf knelpunten die in §1 worden opgelost gelden specifiek voor de audit-pijplijn. `woo-avg-toets` en `stop-slop` hebben hun eigen kwaliteitsproces; zij kunnen als standalone skill worden aangeroepen zonder de andere fases te doorlopen.

---

## 5. Multi-jurisdictie

De skills in deze distributie ondersteunen `jurisdiction: NL,EU,EHRM`. Bij conflicten tussen uitspraken uit verschillende jurisdicties geldt de hiërarchie EHRM > EU > NL. Zie `skills/documenten-audit/references/jurisdiction-hierarchy.md` voor de volledige procedure en conflictregels.

## 6. Externe hulpmiddelen (optioneel)

Deze pijplijn kan optioneel worden aangevuld met externe, losstaande scripts. Deze scripts maken **geen deel uit** van deze distributie en worden niet meegepackaged in de `.skill`-bestanden — het zijn hulpmiddelen die de gebruiker zelf, buiten de skill om, kan draaien tussen de fases.

### ECLI's ophalen tussen Fase 1 en Fase 2

Fase 1's Stap 10 (Manifest Template) levert een lijst van benodigde ECLI's, maar geen bronbestanden zelf — de gebruiker moet die zelf aanleveren. Een extern script (`ecli_lookup_V10.py`, niet onderdeel van deze repo) kan dat ophalen voor NL/EU/EHRM-uitspraken:

1. Zet de ECLI-keys uit Fase 1's manifest-JSON om naar een platte lijst, één ECLI per regel (`eclis.txt`) — het script verwacht dit formaat, niet de JSON-vorm van Stap 10.
2. Draai het script; het levert per ECLI een "normalized JSON"-bestand op (met o.a. een `tekst_waarschuwing`-veld met waarde `LEGE_TEKST`/`KORTE_TEKST`/leeg, en `instantie`/`datum`/`rechtsgebied`-velden).
3. Gebruik deze normalized JSON-bestanden, of het script's eigen manifest-bestand, rechtstreeks als bronbijlage(n) bij Fase 2. Zie `ecli-verificatie/references/source-handling.md` voor hoe Fase 2 met beide manifestvormen omgaat.

### ECLI's cross-checken in Fase 1

Een extern script kan brondocumenten scannen op ECLI-vermeldingen (regex-gebaseerd, geen LLM) als objectieve cross-check op Stap 9's extractie. Zie `documenten-audit/references/ecli-scanner-crosscheck.md`.
