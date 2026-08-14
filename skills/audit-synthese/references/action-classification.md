# Action Classification — Stap 3 (Actielijst)
> Bijbehorende regel in SKILL.md: `<rules>` laatste twee punten.

## Classificatie-matrix

De actie wordt bepaald door de combinatie van `oordeel` en `extractie_zekerheid` uit de verificatie-JSON, plus (voor `NIET_CONTROLEERBAAR`) de waarde van `ecli` en `ecli_formaat_geldig`.

| Oordeel uit verificatie | Extractie_Zekerheid | ECLI-situatie | Actie-classificatie |
|---|---|---|---|
| BEVESTIGD | HOOG / MIDDEN | willekeurig | Geen actie |
| BEVESTIGD | LAAG | willekeurig | "Herformuleer bewering ondanks steun (extractie was vaag)" |
| GEDEELTELIJK | willekeurig | willekeurig | "Nuanceer bewering Z conform <vindplaats>" |
| NIET_BEVESTIGD | HOOG / MIDDEN | willekeurig | "Heroverweeg bewering of zoek betere bron" |
| NIET_BEVESTIGD | LAAG | willekeurig | "Bewering herschrijven: originele extractie was te vaag" |
| TEGENGESPROKEN | willekeurig | willekeurig | "Verwijder of vervang bewering Z" (hoogste prioriteit) |
| NIET_CONTROLEERBAAR | willekeurig | `ecli = "N/A"` | "Bron zoeken en toevoegen" |
| NIET_CONTROLEERBAAR | willekeurig | `ecli ≠ "N/A"` EN `ecli_formaat_geldig = false` | "ECLI corrigeren (formaatfout) en bron opnieuw zoeken" |
| NIET_CONTROLEERBAAR | willekeurig | `ecli ≠ "N/A"` EN `ecli_formaat_geldig = true` | "Bron ophalen en opnieuw verifiëren" |

### Toelichting: BEVESTIGD + LAAG

Zelfs als een bron de bewering toevallig ondersteunt, was de oorspronkelijke extractie vaag. Dat betekent dat de bewering in het brondocument onduidelijk was geformuleerd — mogelijk te algemeen, te absoluut, of zonder noodzakelijke nuance. Herformulering verbetert de leesbaarheid en voorkomt dat een latere, scherper geformuleerde variant van dezelfde bewering onverifieerbaar blijkt.

## Gerelateerde claims — één bewering, meerdere ECLI's

Fase 1 splitst een bewering die op meerdere uitspraken steunt over meerdere rijen met een eigen `Claim_ID`, gekoppeld via de kolom `Gerelateerde_Claims` (zie `claim-register-schema.md` in `documenten-audit`). Fase 2 verifieert elke rij **onafhankelijk** en kent per rij een eigen oordeel toe; het combineren van die oordelen is daarom werk voor Fase 3.

De kolom `Gerelateerde_Claims` staat niet in de verificatie-JSON — lees haar uit het Claim Register in de aangeleverde audit-markdown.

Bepaal per groep:

| Situatie binnen de groep | Actie-classificatie | Prioriteit |
|---|---|---|
| Alle claims `BEVESTIGD` | Geen actie; bewering rust op meerdere bronnen | Laag |
| Oordelen lopen uiteen, waarvan minstens één `TEGENGESPROKEN` | "Bronnenconflict oplossen: bron X bevestigt de bewering, bron Y spreekt haar tegen — bepaal welke uitspraak leidend is" | Hoog |
| Oordelen lopen uiteen zonder `TEGENGESPROKEN` (bijv. `BEVESTIGD` + `NIET_BEVESTIGD`) | "Bewering terugbrengen tot wat de bevestigende bron daadwerkelijk draagt; niet-steunende bron schrappen" | Midden |
| Geen enkele claim in de groep is controleerbaar | Volg de gewone `NIET_CONTROLEERBAAR`-regels per rij | conform tabel hierboven |

Bij een jurisdictieconflict binnen de groep (bijv. een NL-bron bevestigt, een EU-bron spreekt tegen) geldt de hiërarchie EHRM > EU > NL — zie `jurisdiction-hierarchy.md` in `documenten-audit`.

Noem in de actielijst alle betrokken `Claim_ID`'s in één regel in plaats van per rij een losse actie; anders leest de eindredacteur hetzelfde probleem meerdere keren.

## Prioritering

Binnen de actielijst geldt de volgende prioriteitsvolgorde (hoog → laag):

1. **Hoog** — TEGENGESPROKEN claims (onjuiste beweringen actief verwijderen).
2. **Hoog** — NIET_CONTROLEERBAAR met `ecli_formaat_geldig = false` (vermoedelijke hallucinatie of typfout; mogelijk moet de hele claim worden herzien).
3. **Midden** — NIET_BEVESTIGD met HOOG/MIDDEN extractie_zekerheid (bewering lijkt sterk geformuleerd maar wordt niet gesteund — heroverwegen).
4. **Midden** — NIET_CONTROLEERBAAR met geldige ECLI maar ontbrekende bron (bron ophalen is haalbaar).
5. **Midden** — NIET_CONTROLEERBAAR met `ecli = "N/A"` (dragende bewering zonder bron — al dan niet bron vinden).
6. **Laag** — GEDEELTELIJK (nuancering volstaat).
7. **Laag** — NIET_BEVESTIGD met LAAG extractie_zekerheid (bewering was al vaag — herschrijven is genoeg).
8. **Laag** — BEVESTIGD met LAAG extractie_zekerheid (bewering wordt gesteund maar was vaag geformuleerd — herformuleren voor leesbaarheid).

## Voorbeelden

- **TEGENGESPROKEN + HOOG** → "Verwijder bewering over opzegtermijn (C014)" — Hoog.
- **NIET_CONTROLEERBAAR + LAAG + `ecli = "ECLI:NL:HR:23:1"` + `ecli_formaat_geldig = false`** → "ECLI corrigeren (jaartal moet 4 cijfers zijn) en bron opnieuw zoeken voor C003" — Hoog.
- **NIET_CONTROLEERBAAR + MIDDEN + `ecli = "N/A"`** → "Bron zoeken en toevoegen voor stelling zonder ECLI (C007)" — Midden.
- **NIET_CONTROLEERBAAR + HOOG + `ecli = "ECLI:NL:HR:2022:9876"` + `ecli_formaat_geldig = true`** → "Bron ophalen (ECLI:NL:HR:2022:9876) en opnieuw verifiëren voor C004" — Midden.
- **NIET_BEVESTIGD + LAAG** → "Bewering herschrijven: originele extractie was te vaag (C021)" — Laag.
- **GEDEELTELIJK + HOOG** → "Nuanceer bewering conform r.o. 4.2 (C003)" — Laag.
