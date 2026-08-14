# Audit-pijplijn

De taal van de 3-fase pijplijn `documenten-audit` → `ecli-verificatie` → `audit-synthese`. Deze woordenlijst is bindend voor de skill-teksten, de references en de tests; ze bevat geen implementatiedetails.

## Language

**Bewering**:
Eén atomaire juridische stelling uit een brondocument. Een bewering kan door meerdere uitspraken worden onderbouwd en beslaat dan meerdere claims.
_Avoid_: claim (in de betekenis van de stelling zelf), stelling, assertie

**Claim**:
Eén rij in het Claim Register: precies één bewering gekoppeld aan precies één ECLI (of aan `N/A`). De claim is de verificatie-eenheid — Fase 2 verifieert per claim, nooit per bewering.
_Avoid_: rij, verificatie-eenheid, claim-rij

**Claimgroep**:
De verzameling claims die via `Gerelateerde_Claims` aan elkaar hangen en samen één bewering onderbouwen. Alleen Fase 3 ziet de groep als geheel.
_Avoid_: cluster, bundel

**Dragend**:
Een claim is dragend wanneer de bewering die hij onderbouwt voorkomt in de kernconclusie van het document zoals vastgesteld in Stap 1 (Kernantwoord) en Stap 5 (Conclusie). Alle overige claims zijn bijzaak.
_Avoid_: kernclaim, essentieel, doorslaggevend

**Oordeel**:
De uitkomst van Fase 2 voor één claim: `BEVESTIGD`, `GEDEELTELIJK`, `NIET_BEVESTIGD`, `TEGENGESPROKEN` of `NIET_CONTROLEERBAAR`.
_Avoid_: score, resultaat, verdict

**Extractie_Zekerheid**:
Hoe letterlijk de bewering uit het brondocument is overgenomen (`HOOG` / `MIDDEN` / `LAAG`). Zegt niets over de juistheid van de bewering en niets over de geldigheid van de ECLI.
_Avoid_: betrouwbaarheid, confidence, zekerheid

**Kwaliteitsscore**:
De IRAC-score 1–5 die Fase 1 per document toekent op interne kwaliteit. Los van elk oordeel over externe juistheid.
_Avoid_: rating, cijfer

**Gecorrigeerde impact**:
Het label dat Fase 3 aan een document toekent nadat de oordelen zijn verwerkt, volgens de volgordelijke regels in `impact-analysis-rubric.md`.
_Avoid_: eindoordeel, herziene score
