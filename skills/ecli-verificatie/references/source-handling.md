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

## Edge-cases
- **Twijfel over koppeling** → NIET_CONTROLEERBAAR.
- **Bron leeg, onleesbaar, of incompleet** → NIET_CONTROLEERBAAR, tenzij passage ondubbelzinnig.
- **ECLI = "N/A" in Claim Register** → direct NIET_CONTROLEERBAAR (geen zoekactie).
