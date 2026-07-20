# Verwachte Fase 1 output — case-002 (bulk-modus)

> Dit is de **verwachte** output van `documenten-audit` voor `tests/fixtures/case-002/input/docs.md`. Deze casus test specifiek de bulk-modus uit `ecli-verificatie/references/context-budget.md` §4: twee claims uit twee verschillende documenten, gekoppeld aan **dezelfde ECLI**.

## Stap 1: Documentoverzicht

Aanlevering bevatte één ongestructureerde tekst met expliciete `<document id="1">` / `<document id="2">` delimiters. Twee documenten herkend op basis van delimiters.

| Document | Juridische vraag | Rechtsgebied | Kernantwoord | Bronnen | Documenttype |
|---|---|---|---|---|---|
| Document 1 | Mag de sollicitatieplicht tijdelijk worden opgeschort bij ziekte? | socialezekerheidsrecht | Ja, bij ziekte met medische verklaring. | ECLI:NL:CRVB:2024:501 | AI-advies |
| Document 2 | Mag de sollicitatieplicht ook om andere redenen worden opgeschort? | socialezekerheidsrecht | Ja, ook bij mantelzorg (betwiste stelling). | ECLI:NL:CRVB:2024:501 | Bezwaarschrift |

## Stap 2-8: [ingekort — niet relevant voor deze bulk-modus-casus]

## Stap 9: Claim Register

| Claim_ID | Doc_ID | ECLI | Bewering | Extractie_Zekerheid | Opmerking |
|---|---|---|---|---|---|
| C001 | Document 1 | ECLI:NL:CRVB:2024:501 | Bij ziekte, onderbouwd met medische verklaring, moet het UWV de sollicitatieplicht opschorten. | HOOG | |
| C002 | Document 2 | ECLI:NL:CRVB:2024:501 | Het UWV mag de sollicitatieplicht ook opschorten om andere redenen dan ziekte, zoals mantelzorg. | MIDDEN | |

## Stap 10: Manifest Template

```json
{
  "ECLI:NL:CRVB:2024:501": "pad/naar/ECLI_NL_CRVB_2024_501.json"
}
```
