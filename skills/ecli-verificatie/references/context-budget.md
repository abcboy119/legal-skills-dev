# Context Budget — Fase 2 strategie voor grote bronuitspraken
> Bijbehorende sectie in `SKILL.md`: `<verification_unit>` en `<rules>`.

Een HvJ-EU-arrest kan 200+ pagina's zijn; een Hoge Raad-arrest in XML makkelijk 30-50k tokens. Zonder expliciete strategie gaat Fase 2 ofwel claims droppen, ofwel hallucineren dat een passage ontbreekt. Dit document beschrijft hoe je dat voorkomt.

## 1. Basisprincipe: per-claim verificatie-venster

Verifieer **één claim tegelijk**, met een gefocust venster op de bronuitspraak. Niet: hele uitspraak in context laden en dan alle claims in één keer beoordelen. Dat leidt tot oppervlakkige matching en missende vindplaatsen.

Procedure per claim:

1. Lees de atomaire bewering uit het Claim Register.
2. Identificeer 2-4 zoektermen die de bewering karakteriseren (bijv. "dwangsom", "Woo", "vier weken", "verlenging").
3. Zoek in de bronuitspraak naar passages die deze termen bevatten.
4. Bepaal het kleinste venster dat deze passages dekt + ±1 paragraaf context ervoor/erna.
5. Verifieer de bewering uitsluitend binnen dit venster.
6. Noteer de vindplaats (r.o./punt/par.) in de JSON-output.

## 2. Chunking-strategie bij context-overflow

Als het totale venster voor één claim groter is dan ~8k tokens (ruwe schatting), chunk dan op:

1. **Eerste voorkeur: paragraafnummer / r.o.** — Rechterlijke uitspraken hebben vaak expliciete punt- of r.o.-nummers. Chunk per r.o. of per 5 r.o.'s samen.
2. **Tweede voorkeur: secties** — `overwegingen`, `beslissing`, `rechtsoverwegingen`. Chunk per sectie.
3. **Laatste redmiddel: vaste token-grootte** — 4k-token chunks met 500-token overlap. Markeer in `toelichting` dat chunking is gebruikt; vindplaats wordt dan minder precies.

## 3. Volgorde van verificatie

Verifieer claims in de volgende volgorde (hoogste prioriteit eerst):

1. Claims met `Extractie_Zekerheid = HOOG` — deze zijn dragend, moeten eerst.
2. Claims met ECLI's die een manifest hebben (bronbestand aangeleverd) — geen extra zoekkosten.
3. Claims met `Extractie_Zekerheid = MIDDEN`.
4. Claims met `Extractie_Zekerheid = LAAG` — laatst; als context op is, mogen deze `NIET_CONTROLEERBAAR` worden met toelichting *"Context budget uitgeput; claim niet volledig geverifieerd."*

## 4. Bulk-modus: meerdere claims per ECLI

Als meerdere claims aan dezelfde ECLI zijn gekoppeld:

1. Laad de bronuitspraak **één keer** in context.
2. Verifieer claims één voor één binnen dat venster (zie §1).
3. Markeer in `toelichting` als een claim afhankelijk is van een vorige verificatie (bijv. *"Zie ook C001 voor context over de dwangsom."*).
4. Maximum: 10 claims per ECLI per sessie. Boven dit aantal: splitsen in batches en expliciet aangeven in `toelichting` welke batch is gedaan.

## 5. Signalen dat context budget wordt overschreden

Stop of waarschuw als:

- De bronuitspraak > 50k tokens is én er meer dan 5 claims aan gekoppeld zijn.
- Eén claim vereist meer dan 3 chunks om een vindplaats te vinden.
- Het model herhaalt zichzelf of geeft steeds algemenere toelichtingen (signaal van contextverlies).

In die gevallen: markeer resterende claims `NIET_CONTROLEERBAAR` met toelichting *"Context budget overschreden; handmatige verificatie aanbevolen."*

## 6. Wat NIET in context geladen mag worden

- Andere bronuitspraken dan degene die aan de claim is gekoppeld (geen cross-ECLI-contaminatie).
- Eerdere audit-markdown behalve het Claim Register zelf (geen her-audit).
- Webinhoud of externe kennis (al verboden in `<source_handling>`).

## 7. Rapportage

In Stap 1 (Koppeling ECLI en bewering) vermeld je per ECLI kort:

- Geschatte grootte van de bronuitspraak (in tokens of woorden).
- Aantal claims dat eraan is gekoppeld.
- Of chunking is toegepast, en zo ja welke strategie.

Voorbeeld: *"ECLI:NL:HR:2023:1234 — ~12.000 tokens, 3 claims gekoppeld, geen chunking nodig."*

Voorbeeld met chunking: *"ECLI:EU:C:2018:388 — ~45.000 tokens, 7 claims gekoppeld, chunking per r.o.-groepen van 5, claims C014-C017 in batch 1, C018-C020 in batch 2."*
