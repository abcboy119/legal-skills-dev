# Worked example — case-002: bulk-modus (meerdere claims per ECLI)

End-to-end worked example dat specifiek `ecli-verificatie/references/context-budget.md` §4 (bulk-modus) test: **twee claims uit twee verschillende documenten, gekoppeld aan dezelfde ECLI**.

## De casus

Twee korte documenten over de sollicitatieplicht bij een WW-uitkering, die **beide dezelfde uitspraak** aanhalen (`ECLI:NL:CRVB:2024:501`) voor **tegengestelde** conclusies:

1. **Document 1**: opschorting bij ziekte (met medische verklaring) — de bron bevestigt dit.
2. **Document 2**: opschorting ook bij mantelzorg — de bron spreekt dit expliciet tegen (de Raad beperkt de uitzondering tot medische gronden).

## Wat deze casus test

| Concept | Getest door |
|---|---|
| Bulk-modus: meerdere claims aan één ECLI | C001 en C002 delen dezelfde ECLI. |
| Eén bronuitspraak geladen, meerdere keren gebruikt | Beide claims worden onafhankelijk beoordeeld binnen hetzelfde bronvenster. |
| Context-budget.md §4, punt 3: cross-reference in toelichting | C002's `toelichting` verwijst expliciet naar "C001". |
| Tegengestelde oordelen op dezelfde bron | C001 = BEVESTIGD, C002 = TEGENGESPROKEN — laat zien dat "dezelfde bron" niet "hetzelfde oordeel" betekent. |

## Handmatig testen

```bash
python3 scripts/package_skills.py --validate-only
python3 tests/test_pipeline_contracts.py
```
