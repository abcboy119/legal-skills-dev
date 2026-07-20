# JSON Output Schema — Stap 4
> Bijbehorende stap in SKILL.md: Stap 4 (Eindoordeel en JSON-output).
> Machine-leesbaar equivalent: `assets/output.schema.json` (JSON Schema draft 2020-12).

## Schema (per claim)

| Veld | Type | Inhoud |
|---|---|---|
| claim_id | string | uit Claim Register (C001) |
| doc_id | string | uit Claim Register (Document 1) |
| ecli | string | ECLI, of exact `"N/A"` wanneer er geen ECLI is gekoppeld |
| extractie_zekerheid | enum | `HOOG` / `MIDDEN` / `LAAG` — overgenomen uit het Claim Register |
| bron_aangeleverd | boolean | true/false |
| bronbestand | string | pad/bestandsnaam of `""` |
| instantie | string | uit bronmetadata, of `""` |
| datum | string | uit bronmetadata (ISO 8601 `YYYY-MM-DD`), of `""` |
| rechtsgebied | string | uit bronmetadata, of `""` |
| bewering_analyse | string | atomaire bewering, exact overgenomen uit Claim Register |
| oordeel | enum | `BEVESTIGD` / `GEDEELTELIJK` / `NIET_BEVESTIGD` / `TEGENGESPROKEN` / `NIET_CONTROLEERBAAR` |
| vindplaats | string | r.o./punt/par. of `""` |
| broncitaat | string | max ~500 tekens, of `""` |
| relevante_broninhoud | string | korte samenvatting van het citaat |
| toelichting | string | korte toelichting |

## Conventies voor lege / ontbrekende waarden

- Geen ECLI gekoppeld → `ecli: "N/A"` (geen lege string). Fase 3 (`audit-synthese`) checkt op de string `"N/A"` om de juiste actie-classificatie te kiezen.
- Ontbrekend bronbestand → `bronbestand: ""` (lege string).
- `extractie_zekerheid` is verplicht — kopieer het uit het Claim Register; verzin nooit zelf een waarde.

## Self-repair procedure (verplicht, intern)

Voordat je het JSON-codeblok output, doorloop je **in twee passes** de volgende controles:

### Pass 1 — syntactisch
1. Bevat de array exact één JSON-array, geserialiseerd als geldige JSON?
2. Zijn alle strings correct geëscaped (`\n` voor newlines, `\"` voor aanhalingstekens, geen ongeneste backslashes)?
3. Heeft de laatste entry geen trailing comma?

### Pass 2 — semantisch
4. Heeft elke entry alle 15 verplichte velden uit het schema?
5. Heeft elke `oordeel`-waarde één van de vijf toegestane enum-waarden?
6. Heeft elke `extractie_zekerheid`-waarde `HOOG`, `MIDDEN` of `LAAG`?
7. Is elke `ecli`-waarde ofwel een geldige ECLI, ofwel exact `"N/A"`?
8. Komt elke `claim_id` exact overeen met een claim_id uit het aangeleverde Claim Register (geen nieuwe, geen missende)?

### Fallback bij falen

Als Pass 1 of Pass 2 faalt na maximaal twee interne herschrijf-pogingen, output dan **uitsluitend** het volgende codeblok en geen andere tekst:

```json
[
  {
    "claim_id": "_error",
    "doc_id": "_error",
    "ecli": "N/A",
    "extractie_zekerheid": "LAAG",
    "bron_aangeleverd": false,
    "bronbestand": "",
    "instantie": "",
    "datum": "",
    "rechtsgebied": "",
    "bewering_analyse": "self-repair-failed",
    "oordeel": "NIET_CONTROLEERBAAR",
    "vindplaats": "",
    "broncitaat": "",
    "relevante_broninhoud": "",
    "toelichting": "JSON-validatie faalde na 2 pogingen. Handmatige controle vereist."
  }
]
```

Downstream code herkent dit aan `claim_id: "_error"` en kan de menselijke eindredacteur alarmeren.

## Harde eis

PLAATS NA HET JSON-CODEBLOK GEEN ENKELE TEKST, ZELFS GEEN PUNT OF SPATIE. Dit is de absolute afronding van deze skill.
