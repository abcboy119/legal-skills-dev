# Mini-casus 001 — Woo-verzoek en dwangsom

Dit is een kleine, zelf-contained casus om de 3-fase pijplijn end-to-end te testen zonder live LLM-calls. De verwachte tussenresultaten zijn vastgelegd als fixtures, zodat de test kan verifiëren dat de pipeline-contracten kloppen (veldnamen, ECLI-afhandeling, JSON-schema, downstream koppelbaarheid).

## Aanlevering

- `input/docs.md` — twee juridische documenten in één bestand, gescheiden door `<document id="1">` / `<document id="2">` delimiters.
- `sources/ECLI_NL_RBDHA_2023_1234.json` — genormaliseerde JSON van een rechtbankuitspraak.

## Verwachte pijplijn-gedrag

### Fase 1 (documenten-audit) produceert:

- Stap 1: herkent 2 documenten op basis van delimiters.
- Stap 6: IRAC-scores per document (1-5).
- Stap 9 Claim Register met **5 rijen**:
  - `C001` Doc 1, `ECLI:NL:RBDHA:2023:1234`, HOOG — claim over dwangsom bij Woo.
  - `C002` Doc 1, `N/A`, MIDDEN — claim zonder bron.
  - `C003` Doc 2, `ECLI:NL:HR:23:1`, LAAG — **ongeldige ECLI-syntax** (jaartal te kort), moet opmerking krijgen.
  - `C004` Doc 2, `ECLI:NL:HR:2022:9876`, HOOG — claim over Woo-termijn.
  - `C005` Doc 2, `N/A`, LAAG — vage claim.
- Stap 10 Manifest met 2 unieke geldige ECLI's (de ongeldige `ECLI:NL:HR:23:1` mag niet in het manifest, want kan niet gekoppeld worden).

### Fase 2 (ecli-verificatie) produceert:

- Pure JSON-array, 5 entries.
- Elk entry heeft alle 15 verplichte velden volgens `skills/ecli-verificatie/assets/output.schema.json`.
- `extractie_zekerheid` is overgenomen uit Claim Register.
- `ecli` is exact `"N/A"` (geen `""`) voor C002 en C005.
- `ecli` voor C003 is de ongeldige string `"ECLI:NL:HR:23:1"` (zoals in Claim Register), oordeel `NIET_CONTROLEERBAAR` met toelichting over formaat.
- Alleen C001 heeft een aangeleverde bron; C004 niet (ECLI staat niet in manifest); beiden krijgen een passend oordeel.

### Fase 3 (audit-synthese) produceert:

- Impactanalyse-tabel met 2 rijen (Document 1, Document 2).
- Actielijst met minimaal:
  - Hoog-prioriteit actie voor C003 (TEGENGESPROKEN of NIET_CONTROLEERBAAR met ECLI-formaatprobleem).
  - "Bron zoeken en toevoegen" voor C002 en C005 (ECLI = "N/A").
  - "Bron ophalen en opnieuw verifiëren" voor C004 (ECLI ≠ "N/A", bron niet aangeleverd).

## Gebruik

De Python-test in `tests/test_pipeline_contracts.py` valideert deze verwachtingen. Draaien:

```bash
cd /path/to/pipeline_review_fixed2
python3 -m pytest tests/ -v
# of zonder pytest:
python3 tests/test_pipeline_contracts.py
```
