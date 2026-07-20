# Verwachte Fase 3 output — case-002 (bulk-modus)

> Input: `expected_audit.md` (Fase 1) + `expected_verification.json` (Fase 2).

## Stap 1: Impactanalyse per document

| Document | Claims geverifieerd | Bevestigd | Tegengesproken / Niet bevestigd | Niet controleerbaar | Oorspronkelijke score | Gecorrigeerde impact |
|---|---|---|---|---|---|---|
| Document 1 | 1 | 1 | 0 | 0 | n.v.t. (niet uitgewerkt in deze casus) | Oordeel blijft overeind; C001 bevestigd. |
| Document 2 | 1 | 0 | 1 | 0 | n.v.t. (niet uitgewerkt in deze casus) | Fundamenteel verzwakt wegens 1 tegengesproken kernclaim. |

## Stap 2: Gereviseerde conclusie

**Document 1**: Bruikbaar. De kernclaim (C001) over opschorting bij ziekte wordt bevestigd door de Centrale Raad van Beroep.

**Document 2**: Niet bruikbaar in huidige vorm. De kernclaim (C002) over opschorting bij mantelzorg wordt expliciet tegengesproken door dezelfde uitspraak die Document 2 zelf aanhaalt — de Raad beperkt de uitzondering uitdrukkelijk tot medische gronden.

## Stap 3: Actielijst voor eindredacteur

| Prioriteit | Document | Te nemen actie | Claim ID |
|---|---|---|---|
| Hoog | Document 2 | Verwijder bewering over mantelzorg als opschortingsgrond (TEGENGESPROKEN) | C002 |
| Laag | Document 1 | Geen actie; bewering bevestigd door bronuitspraak. | C001 |

## Conclusie

De auditiset is gedeeltelijk betrouwbaar: Document 1 is juridisch bruikbaar, Document 2 moet worden herzien omdat de eigen aangehaalde bron de kernbewering tegenspreekt.
