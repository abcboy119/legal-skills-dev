# Design: ophaalbrug Fase 1→2 en compleet Claim Register

**Status:** voorgesteld — ter review vóór implementatie (reviewronde 1 verwerkt 2026-08-14: drie gaten gedicht, zie §Open punten/vlaggen)
**Datum:** 2026-08-14
**Betrokken skills:** `documenten-audit` (2.1.1 → 2.2.0), `ecli-verificatie` (2.1.1 → 2.2.0), `audit-synthese` (1.2.0 → 1.3.0)
**Bronnen:** `docs/handoff/2026-08-14-research-dan-grilling.md`, `docs/research/2026-08-14-ecli-volledige-uitspraaktekst-nl-eu-ehrm.md`

## Context en doel

Twee vragen stonden open na de v2.1.1/1.2.0-ronde: (1) blijft deze distributie pure prompts of hoort er een ophaalstap bij om het gat tussen Fase 1 (manifest-template, geen bronbestanden) en Fase 2 (verificatie tegen volledige uitspraaktekst) te dichten; (2) wat betekent "dragend" precies — en wat te doen met de dode rubric-regel over bijzaak-claims. Daarnaast lagen vijf contractgaten uit de review van 2026-08-14 op een beslissing.

Vooraf is een primair-bronnenonderzoek gedraaid naar de officiële kanalen voor volledige uitspraaktekst per jurisdictie. Kernbevindingen:

| Jurisdictie | Kanaal | Tekst per ECLI | Belangrijkste risico |
|---|---|---|---|
| NL | Rechtspraak.nl Open Data | Ja, maar ±1 op de 5 ECLI's heeft tekst (>800k mét tekst, ruim 3M alleen metadata) | **Stille lege bron:** metadata-only ECLI geeft HTTP 200 met geldige XML zónder `<uitspraak>`-element |
| EU | EUR-Lex / CURIA | Ja, officieel gedocumenteerde ECLI-permalinks, tekstrijk sinds 1954 | Weinig; SOAP-webservice heeft registratie + limiet (10k resultaten vanaf 1-1-2026) |
| EHRM | HUDOC | Ja, ECLI's aanwezig (retroactief tot 1960) | Machine-endpoints (`/app/query/results`, `/app/conversion/...`) zijn **niet** officieel gedocumenteerd |

## Besluiten (Q1–Q14, grilling 2026-08-14)

| # | Vraag | Besluit |
|---|---|---|
| Q1 | Puur prompts of ophaalstap? | **(a)** Puur prompts + gedocumenteerde ophaalprocedure; extern script blijft optioneel; geen vierde skill |
| Q2 | Dragend/bijzaak-claims? | **(i)** Fase 1 neemt bijzaak-claims óók op, gelabeld in het register |
| Q3 | Waar woont de procedure? | **(a)** Normatief doc in `docs/` + bindende onderdelen inline in de skills |
| Q4 | Lege bron: schema wijzigen? | **(a)** Nee — expliciete detectieregel + vaste toelichting, oordeel `NIET_CONTROLEERBAAR` |
| Q5 | Kolomnaam? | **(a)** `Dragend` met `Ja`/`Nee` |
| Q6 | Manifest en bijzaak-ECLI's? | **(a)** Structuur ongewijzigd; proza markeert bijzaak-ECLI's als optioneel |
| Q7 | Fase 3 en de `_error`-entry? | **(b+)** Twee-gevallenregel: mixed array → entry overslaan + expliciet melden; enige entry → expliciete faalmelding, geen synthese |
| Q8 | `Extractie_Zekerheid` bij formaatfout? | **(a)** Geen `LAAG` meer; veld wordt strikt één-doel; formaatfout reist via Opmerking + `ecli_formaat_geldig` |
| Q9 | Register-vangnet Fase 3? | **(a)** Harde stop, spiegel van Fase 2 |
| Q10 | Rubric telt beweringen? | **(a)** Regels 3 én 4 per bewering (claimgroep = één bewering, zwaarste claim telt) |
| Q11 | Uitwerking Q7 | **Akkoord** met de twee-gevallenregel |
| Q12 | ADR 0002 apart? | **(a)** Ja, eigen ADR |
| Q13 | Bijzaak-voorbeeldrij in case-001? | **(a)** Ja, nieuwe C006 |
| Q14 | Tellen regels 3/4 bijzaak mee? | **(a)** Nee — uitsluitend dragende beweringen; ontbrekende `Dragend`-kolom = alles dragend (oud gedrag) |

## Versiebumps

| Skill | Versie | Bump | Waarom |
|---|---|---|---|
| documenten-audit | 2.1.1 → **2.2.0** | MINOR | bijzaak-claims + `Dragend`-kolom (nieuwe functionaliteit) |
| ecli-verificatie | 2.1.1 → **2.2.0** | MINOR | nieuwe verplichte lege-bron-detectie met vaste output-string |
| audit-synthese | 1.2.0 → **1.3.0** | MINOR | `_error`-afhandeling, register-vangnet, rubric per bewering, levende regel 2 |

Geen MAJOR: `output.schema.json` en `manifest.schema.json` blijven onaangeroerd; de nieuwe registerkolom is backward-compatibel (Fase 2 eist "minstens" de bestaande kolommen; Fase 3-regel: ontbrekende `Dragend`-kolom = alles dragend). `last_updated` → 2026-08-14, alle drie.

## Wijzigingen per skill

### documenten-audit (Fase 1)
1. **Stap 9 (SKILL.md):** bijzaak-claims óók opnemen (niet meer "negeer bijzaak-vermeldingen"); elke rij krijgt `Dragend` (Ja/Nee, per bewering). ECLI-formaatfout → **geen** `LAAG` meer; Opmerking-tekst blijft verplicht (Q8).
2. **claim-register-schema.md:** nieuwe kolom `Dragend` (enum `Ja`/`Nee`); `Extractie_Zekerheid`-richtlijn ontdaan van "of ECLI-formaat is ongeldig" én "of ECLI is afkomstig uit secundaire bron" — het veld wordt strikt één-doel (consequentie van Q8; zie §Open punten voor de striktere lezing).
3. **ecli-format.md:** afhandelingsregel 2 (LAAG zetten) en 4 (LAAG bij secundaire bron) dienovereenkomstig aangepast — Opmerking blijft, LAAG verdwijnt.
4. **claim-register-template.md:** `Dragend`-kolom; format-fout-voorbeeld wordt `HOOG` + Opmerking, plus een apart echt-vaag `LAAG`-voorbeeld.
5. **Stap 10:** manifest-structuur ongewijzigd; proza markeert bijzaak-ECLI's als optioneel op te halen (Q6); verwijzing naar het nieuwe reference-bestand.
6. **Nieuw `references/bronophaal-procedure.md`:** operationele ophaalchecklist (NL/EU/EHRM-endpoints, dekkingswaarschuwing "4 op de 5 NL-ECLI's heeft geen tekst", lege-bron-signalen) — self-contained, geen cross-skill links.

### ecli-verificatie (Fase 2)
7. **source-handling.md + `<source_handling>` in SKILL.md:** expliciete detectieregel voor metadata-only bronnen (controleer op uitspraaktekst/`<uitspraak>`-element vóór verificatie) met vaste toelichting *"Bron zonder uitspraaktekst (alleen metadata) — voor deze ECLI is geen tekst gepubliceerd."* → `NIET_CONTROLEERBAAR`, `bron_aangeleverd` blijft `true`. Geen schema-wijziging (Q4).

### audit-synthese (Fase 3)
8. **SKILL.md:** (i) `_error`-twee-gevallenregel (Q7/Q11); (ii) harde stop bij ontbrekend Claim Register, spiegel van Fase 2 (Q9); (iii) lees `Dragend`-kolom naast `Gerelateerde_Claims`.
9. **impact-analysis-rubric.md:** regel 1/2 gekoppeld aan `Dragend`; regel 2 leeft nu echt; regels 3/4/5 tellen per **dragende** bewering met claimgroep-semantiek (Q10 + Q14); "zwaarste claim binnen de groep" telt.

## Fixtures (case-001 + case-002)
10. `Dragend`-kolom in beide expected_audit-files; **C003 wordt `HOOG`** (letterlijk citaat; de `LAAG` was de formaatfout); nieuwe **C006** (Document 1, bijzaak: "termijn bedraagt in beginsel vier weken, verlengbaar met vier weken", `N/A`, `HOOG`, `Dragend = Nee`). C004 blijft `Dragend = Ja` conform de bestaande fixture-narratief. `expected_verification.json` + C006-entry; `expected_synthese.md`: Document 1 telt 3 claims, impact blijft "Oordeel blijft overeind" (dankzij Q14(a)), actielijst + C006-rij "Bron zoeken en toevoegen"; README's bijgewerkt (tellingen 5→6, C003-tekst). **C004-explicitering (review-gat 3):** `case-001/README.md` krijgt een expliciete regel dat `Dragend=Ja` voor C004 bewust is behouden voor least-surprise (niet een herclassificatie) — de strikte definitie zou hem als bijzaak classificeren; zo leest een toekomstige lezer het niet als bug.

## Tests
11. **Aanpassen:** test 04 (C003 `LAAG`→`HOOG`), test 09 (template-asserties), test 36 waar die de rubric- of registerstrings raakt.
12. **Nieuw (test 37):** contracttest voor deze ronde — `Dragend` in schema+template, Stap 9-bijzaak-tekst + geen-LAAG-bij-formaatfout, Stap 10-optioneel-markering, lege-bron-string in Fase 2, `_error`-regel + register-vangnet in Fase 3, rubric per-bewering + dragend-only, `docs/bronophalen.md` bestaat én is gelinkt vanuit `workflow.md` §6, ADR 0001/0002 bestaan. **Uitkomst-afhankelijke assertie voor de Q8-strikte lezing (review-gat 2):** clausule verwijderd → assert dat `claim-register-schema.md` en `ecli-format.md` "secundaire bron" niet meer als LAAG-trigger bevatten; clausule behouden → assert dat de tekst bestaat maar geen `LAAG` meer forceert. Zo kan een latere agent de zin niet per ongeluk terugzetten zonder dat CI breekt.

## Documentatie en ADR's
13. **`docs/bronophalen.md`** (nieuw): normatieve ophaalprocedure met endpoints, dekkingscijfers, rate limits, licenties, stabiliteitsnotities — elke bewering met URL + raadpleegdatum; verwijst naar het researchbestand. `docs/workflow.md` §6 krijgt de verwijzing (extern script blijft optioneel hulpmiddel).
14. **ADR 0001** en **ADR 0002** (concepten hieronder) — eerste ADR's van deze repo, `docs/adr/` wordt aangemaakt.
15. **CONTEXT.md:** `Dragend` verfijnd (kolom Ja/Nee), nieuwe entries `Bijzaak` en `Lege bron` (teksten hieronder).
16. **CHANGELOG.md:** nieuwe sectie v2.2.0 / 1.3.0 met verwijzing naar research, ADR's en de grilling-besluiten.
17. **MANIFEST-regeneratie** voor alle drie de skills (`generate_manifests.py`).
18. **`README.md`** (review-gat 1): versietabel → 2.2.0 / 2.2.0 / 1.3.0. `sync-checklist.md` eist dit; niets in de teststack controleert het automatisch.
19. *(optioneel, ter beslissing van de gebruiker)* **README-versie-contracttest:** assertie dat de versietabel in `README.md` overeenkomt met de `version:`-frontmatter van de drie SKILL.md's — verheft een handmatig checklist-item tot contracttest conform de repo-filosofie; maakt de README-bump verplicht bij élke versiewijziging (wat de sync-checklist sowieso al eist).

## ADR-concepten

### ADR 0001 — `0001-puur-prompts-met-gedocumenteerde-ophaalprocedure.md`

> De distributie bevat alleen prompts; het gat tussen Fase 1 en Fase 2 (bronbestanden aanleveren) wordt niet gedicht met runtime-code of een vierde skill, maar met een normatieve ophaalprocedure (`docs/bronophalen.md`) plus inline controles in Fase 1 (Stap 10) en Fase 2 (lege-bron-detectie). Onderzoek (docs/research/2026-08-14-…) wees uit dat de kanalen asymmetrisch zijn (NL: ~1 op de 5 ECLI's heeft tekst en lege bronnen zijn stil; EU tekstrijk en officieel; EHRM tekstrijk maar machine-interfaces ongedocumenteerd) — een deterministische ophaalstap zou runtime-code introduceren in een prompt-distributie en het ongedocumenteerde EHRM-kanaal tot onderhoudslast maken, terwijl een vierde skill niet betrouwbaar kan fetchen. Externe scripts blijven optioneel hulpmiddel. Als de procedure in de praktijk te zwaar blijkt, is een meegeleverd script een omkeerbare vervolgstap.

### ADR 0002 — `0002-compleet-claim-register-met-dragend-kolom.md`

> Fase 1 neemt óók bijzaak-claims op in het Claim Register, gelabeld via de kolom `Dragend` (Ja/Nee). Daardoor ziet Fase 3 het volledige beeld van het document, leeft rubric-regel 2 (tegengesproken bijzaak) en kan de impactanalyse kern en bijzaak wegen (regels 3/4 tellen uitsluitend dragende beweringen). Alternatief was een kern-only register (minder werk, maar bijzaak-tegenspraak blijft onzichtbaar). Consequentie: meer rijen → meer verificatiewerk; de ophaalprocedure markeert bijzaak-ECLI's als optioneel.

## CONTEXT.md-wijzigingen

**Dragend** (verfijnd):
> Een claim is dragend wanneer de bewering die hij onderbouwt voorkomt in de kernconclusie van het document zoals vastgesteld in Stap 1 (Kernantwoord) en Stap 5 (Conclusie). In het Claim Register vastgelegd via de kolom `Dragend` (`Ja`/`Nee`). Alle overige claims zijn bijzaak.
> _Avoid_: kernclaim, essentieel, doorslaggevend

**Bijzaak** (nieuw):
> Een claim die niet dragend is (`Dragend = Nee`): de bewering komt niet voor in de kernconclusie. Bijzaak-claims staan wél in het Claim Register; ze beïnvloeden de impactanalyse uitsluitend via rubric-regel 2 en de actielijst.
> _Avoid_: ondergeschikt, terzijde, side-mention

**Lege bron** (nieuw):
> Een aangeleverd bronbestand dat geen uitspraaktekst bevat — alleen metadata (bijv. Rechtspraak-XML zonder `<uitspraak>`-element). Fase 2 kent hiervoor het oordeel `NIET_CONTROLEERBAAR` toe met een vaste toelichting.
> _Avoid_: ontbrekende bron, incomplete bron (dat zijn andere gevallen)

## Uitvoeringsvolgorde en validatie

Volgorde: CONTEXT/ADR's/docs → Fase 1 → Fase 2 → Fase 3 → fixtures → tests → MANIFEST → CHANGELOG. Daarna:

```bash
python3 scripts/package_skills.py --validate-only
python3 tests/test_pipeline_contracts.py   # verwacht: 37 testfuncties, alles groen
python3 scripts/generate_manifests.py --check
```

Bij de eerste failing check wordt gestopt en gerapporteerd; fixes alleen na goedkeuring.

## Open punten / vlaggen

1. **Q8-strikte lezing:** dit plan verwijdert óók de `LAAG`-clausule "ECLI is afkomstig uit secundaire bron" (uit `claim-register-schema.md` en `ecli-format.md`), omdat dat dezelfde veldvervuiling is als de formaatfout. Als de secundaire-bron-clausule moet blijven, geef dit aan vóór implementatie. **Beslissing vereist van de gebruiker; de uitkomst wordt hoe dan ook gepind in test 37 (uitkomst-afhankelijke assertie).**
2. **C004-narratief:** de strikte `Dragend`-definitie zou C004 (bewering niet in de kernconclusie) als bijzaak classificeren, maar de fixture-narratief documenteert hem als dragende claim. Dit plan laat C004 op `Ja` staan (least surprise) en legt die keuze expliciet vast in `case-001/README.md` (review-gat 3); herlabelen blijft een aparte, bewuste keuze.
3. **Commit-strategie:** ~~de v2.1.1/1.2.0-ronde is nog ongecommit~~ — opgelost 2026-08-14: gebruiker gaf opdracht te committen en te pushen; beide rondes zijn gecommit (zie git-historie).
