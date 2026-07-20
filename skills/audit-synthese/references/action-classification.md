# Action Classification — Stap 3 (Actielijst)
> Bijbehorende regel in SKILL.md: `<rules>` laatste twee punten.

## Classificatie-matrix
| Oordeel uit verificatie | Extractie_Zekerheid uit audit | Actie-classificatie |
|---|---|---|
| BEVESTIGD | willekeurig | Geen actie |
| GEDEELTELIJK | willekeurig | "Nuanceer bewering Z conform <vindplaats>" |
| NIET_BEVESTIGD | HOOG / MIDDEN | "Heroverweeg bewering of zoek betere bron" |
| NIET_BEVESTIGD | LAAG | "Bewering herschrijven: originele extractie was te vaag" |
| TEGENGESPROKEN | willekeurig | "Verwijder of vervang bewering Z" (hoogste prioriteit) |
| NIET_CONTROLEERBAAR | willekeurig, ECLI ≠ "N/A" | "Bron ophalen en opnieuw verifiëren" |
| NIET_CONTROLEERBAAR | ECLI = "N/A" | "Bron zoeken en toevoegen" |
