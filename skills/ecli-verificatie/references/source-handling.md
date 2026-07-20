# Source Handling — bronkoppeling en edge-cases
> Bijbehorende sectie in SKILL.md: `<source_handling>`.

## Koppelingshiërarchie (voorkeur hoog → laag)
1. **Manifest** — als een manifestbestand is aangeleverd, gebruik dit als primaire koppeling ECLI → bronbestand.
2. **Normalized JSON** — als voor een ECLI zowel raw XML/HTML als normalized JSON is aangeleverd, gebruik de normalized JSON als primaire verificatiebron.
3. **ECLI-patroon in bestand** — zonder manifest en normalized JSON: zoek in de ruwe tekst van XML-/HTML-bestanden of in de bestandsnaam naar `ECLI:`.

## Wanneer geldt een bron als aangeleverd?
Alleen als minstens één van de volgende geldt:
1. Het manifest koppelt de ECLI expliciet aan een bronbestand; of
2. Het bronbestand bevat zelf de exacte ECLI in metadata of tekst; of
3. De bestandsnaam bevat een duidelijk gesanitized equivalent, zoals `ECLI_EU_C_2018_388`.

## Conflict-resolutie: raw XML/HTML vs normalized JSON

Soms zijn voor één ECLI zowel de raw XML/HTML als een normalized JSON aangeleverd, en **wijken de twee inhoudelijk van elkaar af** (bijv. normalized JSON is per ongeluk getruncteerd, bevat een verkeerde datum, of mist een paragraaf). In dat geval geldt de volgende procedure:

1. **Normalisatie-controle** — vergelijk de ECLI, instantie, datum en uitspraaktekst-lengte tussen raw en normalized. Kleine verschillen (whitespace, tag-style) mogen worden genegeerd; materiële verschillen (andere datum, ontbrekende r.o.) niet.
2. **Bij twijfel: raw wint.** De raw XML/HTML is de primaire bron. Verifieer in raw, en markeer in `toelichting`: *"Normalized JSON wijkt af van raw XML — verificatie gebaseerd op raw."*
3. **Bij grote discrepantie** (normalized mist > 20% van de tekst): vertrouw de normalized JSON niet, verifieer uitsluitend in raw, en voeg een aparte waarschuwing toe aan `toelichting`: *"Normalized JSON incompleet — handmatige controle van normalisatie-proces aanbevolen."*
4. **Beide onvolledig of onleesbaar** → `NIET_CONTROLEERBAAR` met toelichting *"Zowel raw als normalized bron incompleet."*

### Voorbeelden

| Situatie | Actie |
|---|---|
| Raw = 12 r.o.'s, normalized = 12 r.o.'s, kleine whitespace-verschillen | Verifieer in normalized (voorkeur); geen melding. |
| Raw = 12 r.o.'s, normalized = 10 r.o.'s (2 ontbreken) | Verifieer in raw; toelichting: *"Normalized JSON mist 2 r.o.'s — verificatie op raw."* |
| Raw = geldige XML, normalized = `{"tekst_waarschuwing": "LEGE_TEKST"}` | Verifieer in raw; toelichting: *"Normalized JSON is LEGE_TEKST — verificatie op raw."* |
| Raw = 12 r.o.'s, normalized = 12 r.o.'s maar datum wijkt af | Verifieer in raw; toelichting: *"Datum-conflict tussen raw (2023-09-15) en normalized (2023-09-12) — raw genomen."* |

## Edge-cases
- **Geen herkenbaar Claim Register** → stop direct vóór verificatie begint, meld dit expliciet (zie `<source_handling>` in SKILL.md). Ga niet door met giswerk.
- **Twijfel over koppeling** → NIET_CONTROLEERBAAR.
- **Bron leeg, onleesbaar, of incompleet** → NIET_CONTROLEERBAAR, tenzij passage ondubbelzinnig.
- **ECLI = "N/A" in Claim Register** → direct NIET_CONTROLEERBAAR (geen zoekactie).
- **ECLI ongeldig formaat** (bijv. `ECLI:NL:HR:23:1`) → `ecli_formaat_geldig: false` en NIET_CONTROLEERBAAR met toelichting. Zie `references/ecli-format.md` in `documenten-audit`.
- **ECLI buiten ondersteunde jurisdictie** (landcode niet `NL`, `EU` of `CE`) → `NIET_CONTROLEERBAAR` met toelichting "ECLI buiten scope van deze distributie (jurisdiction: NL,EU,EHRM)". Zie `jurisdiction-hierarchy.md` in `documenten-audit`.
- **Bron groter dan context-budget** → pas chunking toe volgens `references/context-budget.md`.
