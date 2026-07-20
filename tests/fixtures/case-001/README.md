# Worked example — case-001: Woo-verzoek en dwangsom

End-to-end worked example voor de 3-fase juridische audit-pijplijn. Dit voorbeeld is zelf-contained: alle input, verwachte tussenresultaten en eindresultaat zijn aanwezig, zodat de integratietest de contracten tussen fases kan verifiëren.

## Aanlevering

```
tests/fixtures/case-001/
├── input/
│   ├── docs.md                          # Twee juridische documenten met <document id>-delimiters
│   └── manifest.json                    # ECLI → bronbestand mapping (Fase 1 output)
├── sources/
│   └── ECLI_NL_RBDHA_2023_1234.json     # Genormaliseerde JSON van rechtbankuitspraak
├── expected_audit.md                    # Verwachte Fase 1 output (Claim Register, manifest)
├── expected_verification.json           # Verwachte Fase 2 output (5 claims, pure JSON)
└── expected_synthese.md                 # Verwachte Fase 3 output (impactanalyse, actielijst)
```

## De casus

Twee korte juridische documenten:

1. **Document 1** (AI-advies, 2024-03-12): Advies over de mogelijkheid van een dwangsom bij niet-tijdige Woo-beantwoording. Verwijst naar `ECLI:NL:RBDHA:2023:1234` (rechtbank Den Haag, dwangsom €500/week). Bevat ook een bronloze bewering over het ontbreken van een wettelijk maximum.

2. **Document 2** (bezwaarschrift, 2024-04-02): Stelt dat de Woo-termijn zes weken bedraagt (niet vier). Verwijst naar `ECLI:NL:HR:23:1` (met opzettelijke typefout in jaartal — moet `2023` zijn, niet `23`) en `ECLI:NL:HR:2022:9876`.

## Verwachte pipeline-gedrag

### Fase 1 (documenten-audit) → `expected_audit.md`

- **Stap 1**: herkent 2 documenten op basis van `<document id>`-delimiters.
- **Stap 6**: IRAC-scores: Document 1 = sterk (4/4/4/4/2/4), Document 2 = zwak (3/2/2/2/1/2).
- **Stap 9 Claim Register**: 5 rijen:
  - `C001` — Doc 1, `ECLI:NL:RBDHA:2023:1234`, HOOG. Geldige ECLI, dragende claim.
  - `C002` — Doc 1, `N/A`, MIDDEN. Bronloze stelling over wettelijk maximum.
  - `C003` — Doc 2, `ECLI:NL:HR:23:1`, LAAG. **Ongeldige ECLI-syntax** (jaartal 2 cijfers). Opmerking verplicht.
  - `C004` — Doc 2, `ECLI:NL:HR:2022:9876`, HOOG. Geldige ECLI, dragende claim.
  - `C005` — Doc 2, `N/A`, LAAG. Vage stelling over nalatigheid.
- **Stap 10 manifest**: alleen de 2 geldige ECLI's (C001 en C004); C003 niet opgenomen.

### Fase 2 (ecli-verificatie) → `expected_verification.json`

- Pure JSON-array, 5 entries, alle 16 velden per entry.
- `extractie_zekerheid` overgenomen uit Claim Register.
- `ecli_formaat_geldig`: `true` voor C001/C004, `false` voor C002/C003/C005.
- `ecli = "N/A"` exact (geen lege string) voor C002 en C005.
- `ecli = "ECLI:NL:HR:23:1"` (string behouden, niet gedropt) voor C003.
- Oordelen:
  - C001 → `BEVESTIGD` (bron aangeleverd, bewering volgt uit r.o. 4.2).
  - C002 → `NIET_CONTROLEERBAAR` (geen ECLI).
  - C003 → `NIET_CONTROLEERBAAR` (ongeldig ECLI-formaat, toelichting vermeldt dit).
  - C004 → `NIET_CONTROLEERBAAR` (geldig ECLI maar geen bronbestand aangeleverd).
  - C005 → `NIET_CONTROLEERBAAR` (geen ECLI).

### Fase 3 (audit-synthese) → `expected_synthese.md`

- **Impactanalyse**: Document 1 = "Oordeel blijft overeind" (1 BEVESTIGD, 1 NIET_CONTROLEERBAAR); Document 2 = "Betrouwbaarheid onvaststelbaar" (3/3 NIET_CONTROLEERBAAR).
- **Actielijst** (geprioriteerd volgens `action-classification.md`):
  - Hoog — C003: ECLI corrigeren en bron opnieuw zoeken.
  - Midden — C004: Bron ophalen en opnieuw verifiëren.
  - Midden — C002: Bron zoeken en toevoegen.
  - Midden — C005: Bron zoeken en toevoegen.
  - Laag — C001: Geen actie.

## Wat deze casus test

| Concept | Getest door |
|---|---|
| ECLI-formaatcontrole (K5) | C003 heeft ongeldige ECLI; mag niet stil verdwijnen. |
| `ecli_formaat_geldig` boolean (K2 bonus) | C001/C004 = true, C002/C003/C005 = false. |
| `ecli = "N/A"` exact (B3) | C002, C005; geen lege strings. |
| `extractie_zekerheid` doorgifte (B2) | Elke entry heeft HOOG/MIDDEN/LAAG uit Claim Register. |
| Action-matrix 7 rijen (P4) | Behalve BEVESTIGD+LAAG zijn alle combinaties aanwezig. |
| Zelf-repair fallback (K1) | Niet in casus — apart getest in test_pipeline_contracts.py. |
| Disclaimer aanwezig (K9) | Niet in casus — apart getest. |
| Compatibility-versies (K10) | Niet in casus — apart getest. |

## Handmatig testen

```bash
# 1. Validator draaien
python3 scripts/package_skills.py --validate-only

# 2. Integratietest draaien
python3 tests/test_pipeline_contracts.py

# 3. End-to-end met echte LLM (handmatig)
#    - Open tests/fixtures/case-001/input/docs.md + manifest.json in Claude Code
#    - Roep /documenten-audit aan
#    - Vergelijk output met expected_audit.md
#    - Aan Fase 2: voeg expected_audit.md + sources/ECLI_NL_RBDHA_2023_1234.json toe
#    - Roep /ecli-verificatie aan
#    - Vergelijk output met expected_verification.json
#    - Roep /audit-synthese aan met audit-markdown + verificatie-JSON
#    - Vergelijk output met expected_synthese.md
```
