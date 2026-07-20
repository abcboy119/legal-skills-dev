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
- `references/claim-register-schema.md` (Kolomdefinities, Extractie_Zekerheid)
- `references/agentic-file-parsing.md` (Hoe meerdere docs te scheiden)
- `assets/manifest-template.json` (JSON template voor Fase 2 input)
- `assets/claim-register-template.md` (Markdown template voor output)

### Fase 2: ecli-verificatie
- `SKILL.md` (4 stappen, streng naar pure JSON)
- `references/source-handling.md` (Manifest, raw vs normalized JSON, N/A afhandeling)
- `references/judgment-definitions.md` (De 5 oordelen met voorbeelden)
- `references/json-output-schema.md` (Velden, self-repair procedure, harde stop-regel)
- `assets/json-output-example.json` (Voorbeeld van verwachte output)

### Fase 3: audit-synthese
- `SKILL.md` (3 stappen, impactanalyse naar actielijst)
- `references/impact-analysis-rubric.md` (Classificatie van "Gecorrigeerde impact")
- `references/action-classification.md` (Matrix: Oordeel + Extractie_Zekerheid -> Actie)
- `assets/action-list-template.md` (Template voor de eindredacteur)

---

## 3. Gedeelde Conventies
Zie `docs/conventions.md` voor de gestandaardiseerde YAML-frontmatter (zoals `jurisdiction`, `version`), hybride descriptions, en JSON-escaping regels.
