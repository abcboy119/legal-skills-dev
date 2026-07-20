# Verwachte Fase 3 output — case-001

> Dit is de **verwachte** output van `audit-synthese` voor `tests/fixtures/case-001/`. Input: `expected_audit.md` (Fase 1) + `expected_verification.json` (Fase 2).

## Stap 1: Impactanalyse per document

| Document | Claims geverifieerd | Bevestigd | Tegengesproken / Niet bevestigd | Niet controleerbaar | Oorspronkelijke score | Gecorrigeerde impact |
|---|---|---|---|---|---|---|
| Document 1 | 2 | 1 | 0 | 1 | sterk (4/4/4/4/2/4) | Oordeel blijft overeind; C001 bevestigd, C002 onverifieerbaar wegens ontbrekende bron. |
| Document 2 | 3 | 0 | 0 | 3 | zwak (3/2/2/2/1/2) | Betrouwbaarheid onvaststelbaar wegens ontbrekende bronnen (3/3 NIET_CONTROLEERBAAR). |

## Stap 2: Gereviseerde conclusie

**Document 1**: Bruikbaar. De kernclaim (C001) over de dwangsom wordt bevestigd door de rechtbankuitspraak; alleen de stelling over het ontbreken van een wettelijk maximum (C002) is onverifieerbaar omdat geen bron is aangeleverd.

**Document 2**: Niet bruikbaar in huidige vorm. Geen van de drie claims is verifieerbaar — C003 wegens ongeldig ECLI-formaat, C004 wegens ontbrekend bronbestand, C005 wegens ontbrekende ECLI. Het bezwaarschrift moet juridisch worden herzien met correcte bronverwijzingen.

## Stap 3: Actielijst voor eindredacteur

| Prioriteit | Document | Te nemen actie | Claim ID |
|---|---|---|---|
| Hoog | Document 2 | ECLI corrigeren (jaartal moet 4 cijfers zijn) en bron opnieuw zoeken; vermoedelijke hallucinatie of typ fout in oorspronkelijke bewering. | C003 |
| Midden | Document 2 | Bron ophalen (ECLI:NL:HR:2022:9876) en opnieuw verifiëren. | C004 |
| Midden | Document 1 | Bron zoeken en toevoegen voor stelling zonder ECLI (geen wettelijk maximum dwangsom). | C002 |
| Midden | Document 2 | Bron zoeken en toevoegen voor stelling zonder ECLI (nalatigheid overheid). | C005 |
| Laag | Document 1 | Geen actie; bewering bevestigd door bronuitspraak. | C001 |

## Conclusie

De auditiset is deels betrouwbaar: Document 1 is juridisch bruikbaar na aanvulling van één bron, Document 2 moet worden herzien vanwege een ongeldige ECLI en ontbrekende bronnen.
