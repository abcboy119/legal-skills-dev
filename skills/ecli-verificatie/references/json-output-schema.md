# JSON Output Schema — Stap 4
> Bijbehorende stap in SKILL.md: Stap 4 (Eindoordeel en JSON-output).

## Schema (per claim)
| Veld | Type | Inhoud |
|---|---|---|
| claim_id | string | uit Claim Register (C001) |
| doc_id | string | uit Claim Register (Document 1) |
| ecli | string | ECLI of "" bij N/A |
| bron_aangeleverd | boolean | true/false |
| bronbestand | string | pad/bestandsnaam of "" |
| instantie | string | uit bronmetadata, of "" |
| datum | string | uit bronmetadata, of "" |
| rechtsgebied | string | uit bronmetadata, of "" |
| bewering_analyse | string | atomaire bewering |
| oordeel | enum | BEVESTIGD / GEDEELTELIJK / NIET_BEVESTIGD / TEGENGESPROKEN / NIET_CONTROLEERBAAR |
| vindplaats | string | r.o./punt/par. of "" |
| broncitaat | string | max ~500 tekens, of "" |
| relevante_broninhoud | string | korte samenvatting van het citaat |
| toelichting | string | korte toelichting |

## Self-repair (verplicht, intern)
Voordat je de JSON genereert, controleer intern:
1. Exact één geldige JSON-array, en niets anders na het codeblok?
2. Alle strings correct geëscaped?
3. Laatste entry in de array heeft geen trailing comma?

## Harde eis
PLAATS NA HET JSON-CODEBLOK GEEN ENKELE TEKST, ZELFS GEEN PUNT OF SPATIE.
