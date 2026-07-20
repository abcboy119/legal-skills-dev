# Claim Register Schema

> Kolomdefinities voor het Claim Register zoals geproduceerd in Stap 9 van `documenten-audit`.
> Verbruikt door Fase 2 (`ecli-verificatie`) en Fase 3 (`audit-synthese`).

## Kolommen

| Kolom | Type | Waarden |
|---|---|---|
| Claim_ID | string | `C001`, `C002`, … (opeenvolgend, uniek binnen de audit) |
| Doc_ID | string | `Document 1`, `Document 2`, … (komt overeen met Stap 1) |
| ECLI | string | Geldige ECLI (zie regex hieronder) of exact `N/A` |
| Bewering | string | Atomaire stelling — één duidelijke juridische claim per rij |
| Extractie_Zekerheid | enum | `HOOG` / `MIDDEN` / `LAAG` |
| Opmerking | string (optioneel) | Vrije tekst, bijv. opmerkingen over ECLI-formaat of extractie-twijfel |
| Gerelateerde_Claims | string (optioneel) | Kommagescheiden lijst van andere Claim_ID's die dezelfde bewering onderbouwen met een andere ECLI (bijv. `C006, C007`) — zie §Meerdere ECLI's per claim hieronder |

## ECLI-formaat

Geldige ECLI's voldoen aan:

```regex
^ECLI:[A-Z]{2}:[A-Z0-9]+:\d{4}:[A-Za-z0-9.]+$
```

Voorbeelden: `ECLI:NL:HR:2023:1234`, `ECLI:EU:C:2018:388`.

Zie `references/ecli-format.md` voor de volledige regels, voorbeelden van ongeldige ECLI's, en de afhandeling bij ongeldige syntaxis.

## Extractie_Zekerheid — richtlijnen

- **HOOG** — bewering is letterlijk of bijna-letterlijk uit het document genomen, met duidelijke koppeling aan ECLI en vindplaats.
- **MIDDEN** — bewering is een correcte parafrase, maar er is enige interpretatie nodig om van brontekst naar atomaire claim te komen.
- **LAAG** — bewering is geïnterpreteerd of samengevat; meerdere lezingen mogelijk; of ECLI-formaat is ongeldig; of ECLI is afkomstig uit secundaire bron.

## Atomaire bewering — wat telt als één claim?

- Één juridische stelling met één onderwerp (bijv. *"De opzegtermijn bedraagt één maand bij een arbeidsovereenkomst voor onbepaalde tijd."*).
- Niet combineren: *"De opzegtermijn bedraagt één maand en de werkgever hoeft geen redenen te geven."* is **twee** claims (C001 + C002).
- Bronloze stellingen zijn toegestaan (ECLI = `N/A`), maar worden in Fase 2 automatisch `NIET_CONTROLEERBAAR`.

## Meerdere ECLI's per claim — conventie

Het Claim Register staat maar één ECLI per rij toe. Als een bewering wordt onderbouwd door **meerdere** uitspraken (bijv. "vaste rechtspraak"), splits die bewering dan over meerdere rijen:

- Gebruik voor elke ondersteunende ECLI een aparte rij met een **eigen** `Claim_ID`, maar **dezelfde** `Bewering`-tekst.
- Koppel de rijen aan elkaar via de kolom `Gerelateerde_Claims`: elke rij verwijst naar de `Claim_ID`'s van de andere rijen in dezelfde groep.

Voorbeeld: een bewering onderbouwd door twee uitspraken wordt C006 (ECLI A, Gerelateerde_Claims = "C007") en C007 (ECLI B, Gerelateerde_Claims = "C006"). Fase 2 verifieert beide rijen onafhankelijk — het is aan Fase 3 (`audit-synthese`) om bij tegenstrijdige oordelen tussen gerelateerde claims dit te signaleren.

Dit is een **conventie**, geen schema-wijziging: elke rij blijft één zelfstandige, atomaire verificatie-eenheid zoals hierboven gedefinieerd.
