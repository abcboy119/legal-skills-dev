# Overdracht — eerst `/research`, daarna `/grill-with-docs`

> Geschreven 2026-08-14. Bedoeld om in een **verse sessie** te openen. Lees dit bestand volledig, draai dan Stap 1, en pas daarna Stap 2.

## Wat je moet doen

1. **`/research`** met de onderzoeksvraag uit §Onderzoeksopdracht hieronder. Laat de achtergrondagent draaien.
2. **`/grill-with-docs`** met de agenda uit §Grilling-agenda, zodra het researchbestand er is.

Draai ze in deze volgorde. Stap 2 zonder Stap 1 leidt tot een interview over feiten die niemand heeft opgezocht — precies wat we willen vermijden.

---

## Het project in vijf regels

Drie juridische AI-skills (prompts, geen runtime-code) die één pijplijn vormen:

```
documenten-audit (2.1.1) → ecli-verificatie (2.1.1) → audit-synthese (1.2.0)
   Claim Register            pure JSON (16 velden)      impactanalyse + actielijst
```

Doel: voorkomen dat een AI-geschreven juridisch stuk leunt op een ECLI die de bewering niet dekt, of die niet bestaat. De Python in `scripts/` en `tests/` bouwt niets — hij valideert de skill-teksten (196 contract-assertions op letterlijke strings) en packaget ze naar `dist/`.

Zie `CLAUDE.md` voor de harde conventies, `docs/workflow.md` voor het waarom, `CONTEXT.md` voor de woordenlijst.

## Staat van de repo op 2026-08-14

- Alle drie de CI-checks groen: 3/3 skills valid, manifests consistent, **196 PASS / 0 FAIL**.
- **Niet gecommit**: een afgeronde consistentieronde `v2.1.1 / 1.2.0` (7 gecorrigeerde contractfouten, zie `CHANGELOG.md`), plus deze sessie's `CONTEXT.md`, `docs/agents/` en dit bestand.
- `last_updated` staat overal op `2026-07-31`; de conventie in `CLAUDE.md` schrijft "vandaag" voor. Bump dit bij de eerstvolgende inhoudelijke wijziging.
- **Nul ADR's.** Elke eerdere ontwerpkeuze is nergens onderbouwd vastgelegd. `docs/adr/` bestaat nog niet.

## De aanleiding

Deze repo is de "light" variant van `/home/badr/Claude/Projects/legal_agent_cloud` — daar draait een Streamlit/Qdrant-app met **live** ECLI-lookup. Hier levert de gebruiker de bronbestanden handmatig aan.

Dat handmatige gat zit precies tussen Fase 1 en Fase 2: Stap 10 van `documenten-audit` produceert een manifest-template met de benodigde ECLI's, maar geen bronbestanden. `docs/workflow.md` §6 verwijst naar een extern script (`ecli_lookup_V10.py`) dat geen deel uitmaakt van de distributie.

---

## Onderzoeksopdracht (Stap 1)

**Hoofdvraag:** Wat is er anno nu langs officiële, publieke kanalen op te halen aan volledige uitspraaktekst voor NL, EU en EHRM — en wat betekent dat voor het gat tussen Fase 1 en Fase 2?

Werk uitsluitend met **primaire bronnen**: officiële API-documentatie en voorwaarden van de aanbieders zelf, geen blogposts of samenvattingen van derden.

Beantwoord per jurisdictie:

| Jurisdictie | Te onderzoeken kanaal |
|---|---|
| NL | Rechtspraak.nl Open Data (de ECLI-index en de losse-uitspraak-endpoints) |
| EU | EUR-Lex / CURIA — beschikbaarheid van HvJ-EU-uitspraken per ECLI |
| EHRM | HUDOC — of uitspraken per ECLI (`ECLI:CE:ECHR:...`) opvraagbaar zijn |

Voor elk kanaal wil ik weten:

1. **Endpoint en responsformaat** — welke URL, welk formaat terug (XML/JSON/HTML), en of de *volledige* uitspraaktekst erin zit of alleen metadata plus een link.
2. **Dekking en gaten** — welk deel van de uitspraken is daadwerkelijk als tekst beschikbaar. Bij Rechtspraak: welk aandeel ECLI's alleen metadata heeft en geen tekst. Dit is de kern: een pijplijn die stil een lege bron accepteert is erger dan een die niets ophaalt.
3. **Gebruiksvoorwaarden en limieten** — rate limits, authenticatie, hergebruiksvoorwaarden.
4. **Stabiliteit** — is het endpoint recent gewijzigd, is er een versienummer, is er een aangekondigde deprecatie.

**Lever op:** één Markdown-bestand in `docs/research/`, met per bevinding een directe bronverwijzing (URL + datum van raadplegen). Markeer expliciet wat je **niet** hebt kunnen vaststellen — een open vraag is bruikbaar, een gok niet.

**Buiten scope:** implementatie. Geen code schrijven, geen script bouwen. Dit onderzoek levert feiten waarop een keuze wordt gemaakt, niet de keuze zelf.

---

## Grilling-agenda (Stap 2)

Draai `/grill-with-docs` zodra het researchbestand er ligt. Deze vragen staan open; werk ze als design-tree, frontier per ronde.

### De hoofdvraag

Blijft deze distributie **puur prompts** (de gebruiker levert bronnen aan), of hoort er een ophaalstap bij — en zo ja, in welke vorm: een gedocumenteerde procedure, een meegeleverd script, of een vierde skill?

Dit is de keuze waar het onderzoek voor dient. Ze raakt de scope-afbakening in `docs/workflow.md` §4 en §6, en verdient hoe dan ook een **ADR** — de eerste van deze repo.

### Geparkeerde vraag uit de vorige sessie

**Wat betekent "dragend"?** `CONTEXT.md` definieert het nu als: de bewering komt voor in de kernconclusie van het document (Stap 1 Kernantwoord, Stap 5 Conclusie). Dat is vastgelegd, maar de consequentie is niet gekozen:

- Fase 1 Stap 9 zegt *"neem uitsluitend ECLI's op die dragend zijn (negeer bijzaak-vermeldingen)"*.
- De impact-rubric van Fase 3 heeft sinds v1.2.0 een regel 2 over *tegengesproken **bijzaak**-claims* — claims die volgens Fase 1 nooit in het register belanden.

Opties: (i) Fase 1 neemt bijzaak-claims óók op en labelt ze, (ii) regel 1 en 2 van de rubric worden één regel, (iii) laten staan. De gebruiker had hier nog geen voorkeur. Optie (i) is verwant aan de eerder gekozen richting "kolom in het Claim Register, later".

### Bevindingen die op een beslissing wachten

Vijf contractgaten, gevonden op 2026-08-14, zwaarste eerst. Geen enkele is gefixt — de gebruiker koos ervoor eerst het doel scherp te stellen.

1. **Fase 3 vangt de `_error`-entry niet af.** Fase 2 kan bij mislukte self-repair een array met `claim_id: "_error"` produceren (`ecli-verificatie/references/json-output-schema.md`). Die entry heeft alle 16 velden, dus Fase 3's validatieregel laat hem door en synthetiseert vrolijk een impactanalyse van een mislukte run. Stille fout.
2. **`Extractie_Zekerheid` doet twee banen.** Fase 1 zet hem op `LAAG` bij een ECLI-**formaatfout**, ook bij een letterlijk geciteerde bewering (`documenten-audit/SKILL.md` Stap 9). Fase 3 leest `NIET_BEVESTIGD + LAAG` en adviseert *"bewering herschrijven: originele extractie was te vaag"* — fout advies; het veld `ecli_formaat_geldig` draagt die informatie al.
3. **Rubric-regel 2 is dood** — zie de geparkeerde vraag hierboven.
4. **Fase 3 leest het Claim Register zonder vangnet.** Fase 2 stopt hard bij een onherkenbaar register; Fase 3 is er sinds v1.2.0 óók van afhankelijk (`Gerelateerde_Claims`) maar controleert niets. Geen register betekent nu: claimgroepen worden stilzwijgend gemist.
5. **De impact-rubric telt claims, niet beweringen.** *">50% van de claims is NIET_CONTROLEERBAAR"* telt rijen; één bewering met vier gerelateerde claims weegt vier keer zo zwaar als een bewering met één claim.

### Volgorde-advies voor het interview

Behandel de hoofdvraag eerst — bevinding 1 t/m 5 zijn reparaties binnen de huidige architectuur, en als de architectuur verschuift, verschuift hun oplossing mee. Bevinding 1 en 2 produceren *fout* advies (niet slechts onvolledig) en zijn de kandidaten om hoe dan ook te fixen, ongeacht de uitkomst.

## Spelregels bij het wijzigen van een skill

Staan volledig in `CLAUDE.md` en `docs/conventions.md` §7. De vier die het vaakst worden vergeten:

- `version` bumpen is **verplicht**, ook bij een wijziging in `references/`.
- `last_updated` naar vandaag, nooit in de toekomst.
- Na elke wijziging in `references/` of `assets/`: `python3 scripts/generate_manifests.py`, anders faalt CI.
- De tests grepen op **letterlijke strings** in de skill-teksten. Een zin herformuleren breekt regelmatig een test — dat is bedoeld gedrag, geen fout in de test.
