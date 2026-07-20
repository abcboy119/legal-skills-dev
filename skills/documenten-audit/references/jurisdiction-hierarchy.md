# Multi-jurisdictie — hiërarchie en conflictregels
> Bijbehorende veld in frontmatter: `jurisdiction: NL,EU,EHRM`.

De skills in deze distributie ondersteunen juridische documenten uit meerdere jurisdicties. Dit document beschrijft de hiërarchie en hoe conflicten tussen uitspraken uit verschillende jurisdicties worden afgehandeld.

## 1. Hiërarchie (hoog → laag)

1. **EHRM** (Europese Hof voor de Rechten van de Mens) — hoogste autoriteit voor mensenrechtenkwesties (EVRM). Uitspraken bindend voor Nederland.
2. **EU** (Hof van Justitie EU, Gerecht EU) — bindend voor Nederland in EU-rechtsgebieden (o.a. privacyrecht/AVG, interne markt, mededinging).
3. **NL** (Hoge Raad, Gerechtshoven, Rechtbanken) — nationaal recht, dient in overeenstemming te zijn met EHRM en EU-recht.

ECLI-prefixen herkennen:
- `ECLI:CE:ECHR:...` — EHRM.
- `ECLI:EU:C:...`, `ECLI:EU:T:...`, `ECLI:EU:F:...` — HvJ EU, Gerecht EU, EU-ambtenarenrechter.
- `ECLI:NL:HR:...`, `ECLI:NL:GH...:...`, `ECLI:NL:RB...:...` — Hoge Raad, Gerechtshof, Rechtbank.

## 2. Soorten conflicten

| Type conflict | Voorbeeld | Hoe te markeren |
|---|---|---|
| **Direct conflict** — NL-uitspraak in strijd met EU-recht | NL-rechtbank zegt "AVG niet van toepassing"; HvJ EU zegt wel. | `TEGENGESPROKEN` met toelichting over jurisdictieconflict. |
| **EVRM-conflict** — NL-uitspraak in strijd met EVRM | NL-rechtbank staat langdurige detentie zonder toegang tot advocaat toe; EHRM zegt dat dit art. 5/6 EVRM schendt. | `TEGENGESPROKEN` met toelichting. |
| **Voorrangsregel** — EU-recht gaat voor op nationaal recht | Document claimt dat NL-wet X toepasselijk is, terwijl EU-verordening Y dezelfde materie regelt. | `GEDEELTELIJK` of `NIET_BEVESTIGD` met toelichting over voorrangsregel. |
| **Niet-bindende uitspraak** — HvJ EU prejudicieel advies | Document claimt dat HvJ EU "heeft beslist"; eigenlijk was het een prejudiciële vraag. | `GEDEELTELIJK` met toelichting "prejudiciële beantwoording, geen direct bindende uitspraak in deze zaak." |

## 3. Procedure bij vermoedelijk conflict

In Fase 1 (documenten-audit):
- Markeer in Stap 4 (Bronnenanalyse) als er ECLI's uit meerdere jurisdicties worden aangehaald.
- Markeer in Stap 5 (Standpuntenanalyse) als er een mogelijk jurisdictieconflict is tussen de aangehaalde bronnen.

In Fase 2 (ecli-verificatie):
- Verifieer elke claim tegen zijn eigen bron (geen cross-ECLI-comparison).
- Als een claim een NL-bron citeert maar de bewering in strijd is met een EU-bron die ook is aangeleverd: markeer `TEGENGESPROKEN` met toelichting *"NL-bron bevestigt bewering, maar EU-bron ECLI:EU:C:... spreekt dit tegen (voorangsregel EU-recht)."*

In Fase 3 (audit-synthese):
- In de actielijst krijgt een `TEGENGESPROKEN` wegens jurisdictieconflict prioriteit **Hoog**, met actie: *"Herzie bewering in het licht van [EHRM/EU]-uitspraak; NL-bron mag niet worden gevolgd."*

## 4. Speciale regels per jurisdictie

### EHRM
- EHRM-uitspraken zijn **reactief** — zij beoordelen of een lidstaat het EVRM heeft geschonden in een specifieke zaak.
- Margin of appreciation: EHRM geeft lidstaten enige beoordelingsruimte. Een NL-uitspraak hoeft niet automatisch `TEGENGESPROKEN` te zijn als de EHRM een margin of appreciation toepast.
- Pilot-judgment procedure: bij structurele problemen. Markeer in toelichting als een EHRM-uitspraak een pilot-judgment is.

### EU
- HvJ EU prejudiciële uitspraken zijn **bindend** voor alle nationale rechters in de betrokken materie.
- Voorrangsregel: EU-recht (verordeningen direct; richtlijnen na implementatie) gaat boven conflicterend nationaal recht.
- HvJ EU-uitspraken hebben **retroactieve werking** in principe (de uitspraak verklaart wat het recht altijd al was).

### NL
- Hoge Raad: hoogste instantie in civiel, straf en bestuursrecht.
- Gerechtshoven: appel-instantie.
- Rechtbanken: eerste aanleg.
- Een lagere NL-rechter kan een uitspraak van een hogere NL-rechter niet zomaar naast zich neerleggen (vaste rechtspraak). Markeer als dit in een brondocument wel wordt beweerd.

## 5. Voorbeelden van juiste afhandeling

### Voorbeeld 1: Direct EU-NL conflict
- **Claim**: "Logbestanden vallen niet onder het inzagerecht van art. 15 AVG."
- **Bron NL**: Rechtbank stelt dit in 2022.
- **Bron EU**: HvJ EU (C-202/21, 2023) stelt het tegendeel.
- **Oordeel**: `TEGENGESPROKEN` met toelichting: *"NL-bron (2022) bevestigt bewering, maar HvJ EU (2023) spreekt dit tegen. Voorangsregel EU-recht: bewering is onjuist."*

### Voorbeeld 2: EVRM-margin of appreciation
- **Claim**: "Langdurige detentie zonder toegang tot advocaat is toegestaan."
- **Bron NL**: Hoge Raad bevestigt in specifieke zaak.
- **Bron EHRM**: EHRM oordeelt dat dit in beginsel in strijd is met art. 6 EVRM, maar laat lidstaten enige beoordelingsruimte.
- **Oordeel**: `GEDEELTELIJK` met toelichting: *"NL-bron bevestigt bewering binnen nationale context, maar EHRM nuanceert: margin of appreciation, niet absolute toestemming."*

### Voorbeeld 3: Prejudiciële vraag verkeerd geïnterpreteerd
- **Claim**: "HvJ EU heeft bepaald dat X wettelijk is."
- **Bron EU**: HvJ EU beantwoordt prejudiciële vraag over uitleg van een richtlijn.
- **Oordeel**: `GEDEELTELIJK` met toelichting: *"HvJ EU beantwoordt een prejudiciële vraag over uitleg, geen directe uitspraak over wettelijkheid van X in deze zaak."*

## 6. Wat te doen bij onzekerheid

Als de auditor (LLM) niet zeker weet of er sprake is van een jurisdictieconflict:
- Markeer de claim als `NIET_CONTROLEERBAAR` met toelichting *"Mogelijk jurisdictieconflict; handmatige beoordeling door jurist vereist."*
- Vermeld in Stap 4 (Fase 1) dat er ECLI's uit meerdere jurisdicties aanwezig zijn.
- Vermeld in Stap 8 (Fase 1) als lacune dat jurisdictieanalyse nodig is.

De LLM mag geen eigen rechtspraak-creatie doen — alleen vaststellen wat de bronnen zeggen en eventuele conflicten signaleren.
