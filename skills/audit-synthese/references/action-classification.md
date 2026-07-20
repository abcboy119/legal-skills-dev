# Action Classification — Stap 3 (Actielijst)
> Bijbehorende regel in SKILL.md: `<rules>` laatste twee punten.

## Classificatie-matrix

De actie wordt bepaald door de combinatie van `oordeel` en `extractie_zekerheid` uit de verificatie-JSON, plus (voor `NIET_CONTROLEERBAAR`) de waarde van `ecli` en `ecli_formaat_geldig`.

| Oordeel uit verificatie | Extractie_Zekerheid | ECLI-situatie | Actie-classificatie |
|---|---|---|---|
| BEVESTIGD | willekeurig | willekeurig | Geen actie |
| GEDEELTELIJK | willekeurig | willekeurig | "Nuanceer bewering Z conform <vindplaats>" |
| NIET_BEVESTIGD | HOOG / MIDDEN | willekeurig | "Heroverweeg bewering of zoek betere bron" |
| NIET_BEVESTIGD | LAAG | willekeurig | "Bewering herschrijven: originele extractie was te vaag" |
| TEGENGESPROKEN | willekeurig | willekeurig | "Verwijder of vervang bewering Z" (hoogste prioriteit) |
| NIET_CONTROLEERBAAR | willekeurig | `ecli = "N/A"` | "Bron zoeken en toevoegen" |
| NIET_CONTROLEERBAAR | willekeurig | `ecli ≠ "N/A"` EN `ecli_formaat_geldig = false` | "ECLI corrigeren (formaatfout) en bron opnieuw zoeken" |
| NIET_CONTROLEERBAAR | willekeurig | `ecli ≠ "N/A"` EN `ecli_formaat_geldig = true` | "Bron ophalen en opnieuw verifiëren" |

## Prioritering

Binnen de actielijst geldt de volgende prioriteitsvolgorde (hoog → laag):

1. **Hoog** — TEGENGESPROKEN claims (onjuiste beweringen actief verwijderen).
2. **Hoog** — NIET_CONTROLEERBAAR met `ecli_formaat_geldig = false` (vermoedelijke hallucinatie of typfout; mogelijk moet de hele claim worden herzien).
3. **Midden** — NIET_BEVESTIGD met HOOG/MIDDEN extractie_zekerheid (bewering lijkt sterk geformuleerd maar wordt niet gesteund — heroverwegen).
4. **Midden** — NIET_CONTROLEERBAAR met geldige ECLI maar ontbrekende bron (bron ophalen is haalbaar).
5. **Midden** — NIET_CONTROLEERBAAR met `ecli = "N/A"` (dragende bewering zonder bron — al dan niet bron vinden).
6. **Laag** — GEDEELTELIJK (nuancering volstaat).
7. **Laag** — NIET_BEVESTIGD met LAAG extractie_zekerheid (bewering was al vaag — herschrijven is genoeg).

## Voorbeelden

- **TEGENGESPROKEN + HOOG** → "Verwijder bewering over opzegtermijn (C014)" — Hoog.
- **NIET_CONTROLEERBAAR + LAAG + `ecli = "ECLI:NL:HR:23:1"` + `ecli_formaat_geldig = false`** → "ECLI corrigeren (jaartal moet 4 cijfers zijn) en bron opnieuw zoeken voor C003" — Hoog.
- **NIET_CONTROLEERBAAR + MIDDEN + `ecli = "N/A"`** → "Bron zoeken en toevoegen voor stelling zonder ECLI (C007)" — Midden.
- **NIET_CONTROLEERBAAR + HOOG + `ecli = "ECLI:NL:HR:2022:9876"` + `ecli_formaat_geldig = true`** → "Bron ophalen (ECLI:NL:HR:2022:9876) en opnieuw verifiëren voor C004" — Midden.
- **NIET_BEVESTIGD + LAAG** → "Bewering herschrijven: originele extractie was te vaag (C021)" — Laag.
- **GEDEELTELIJK + HOOG** → "Nuanceer bewering conform r.o. 4.2 (C003)" — Laag.
