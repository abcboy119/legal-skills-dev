# ECLI-formaat — validatie en afhandeling
> Bijbehorende stap in `SKILL.md`: Stap 9 (Claim Register).
> Ook gebruikt in Fase 2 (`ecli-verificatie`) bij de bronkoppeling.

## Formele syntaxis

Een geldige ECLI voldoet aan:

```
ECLI:<country>:<court>:<year>:<identifier>
```

- `country` — ISO 3166-1 alpha-2 landcode (2 hoofdletters, bijv. `NL`, `EU`, `BE`, `DE`).
- `court` — afkorting van de uitsprekende instantie (hoofdletters en cijfers, bijv. `HR`, `RB`, `C` voor HvJ-EU, `ECLI`-natieafhankelijk).
- `year` — vier cijfers (jaartal van uitspraak).
- `identifier` — alfanumerieke identifier (letters, cijfers, punten), door de instantie toegekend.

## Regex (voor programmatic gebruik)

```regex
^ECLI:[A-Z]{2}:[A-Z0-9]+:\d{4}:[A-Za-z0-9.]+$
```

Voorbeelden van geldige ECLI's:
- `ECLI:NL:HR:2023:1234` (Hoge Raad)
- `ECLI:NL:RBDHA:2024:5000` (Rechtbank Den Haag)
- `ECLI:EU:C:2018:388` (HvJ-EU)
- `ECLI:EU:T:2019:510` (Gerecht EU)
- `ECLI:NL:GHAMS:2022:2500` (Gerechtshof Amsterdam)

Voorbeelden van ongeldige ECLI's (moeten worden gemarkeerd):
- `ECLI:NL:HR:23:1234` — jaartal moet 4 cijfers zijn.
- `ecli:nl:hr:2023:1234` — moet hoofdletters zijn.
- `ECLI:NL-HR:2023:1234` — geen streepjes in `court`.
- `ECLI:NL:HR:2023:` — identifier ontbreekt.
- `ECLI:NL:HR:2023:AB CD` — spatie in identifier niet toegestaan.
- `NL:HR:2023:1234` — `ECLI:` prefix ontbreekt.

## Afhandeling in Fase 1 (documenten-audit), Stap 9

Bij extractie van claims:

1. **Geldige ECLI** — neem op in het Claim Register met `ECLI`-kolom exact zoals in bron. Gebruik `Extractie_Zekerheid` naar eigen inschatting.
2. **Ongeldige ECLI-syntax** — neem de string toch op (zodat de eindredacteur kan zien wat er stond), maar:
   - Zet `Extractie_Zekerheid = LAAG`.
   - Voeg in een aparte kolom "Opmerking" (of voetnoot bij de rij) de tekst: *"ECLI voldoet niet aan formaat — vermoedelijke typfout of hallucinatie."*
3. **Geen ECLI maar wel een dragende bewering** — neem op met `ECLI = "N/A"`. Fase 2 zal deze automatisch als `NIET_CONTROLEERBAAR` markeren.
4. **ECLI die er uitziet als een ECLI maar in een niet-ECLI-bron staat** (bijv. een citaat uit een wetcommentaar) — neem op met `Extractie_Zekerheid = LAAG` en opmerking *"ECLI genoemd in secundaire bron, niet in primaire uitspraak."*

## Afhandeling in Fase 2 (ecli-verificatie)

- Bij koppeling met bronbestand: controleer dat de ECLI in het Claim Register overeenkomt met de ECLI in bronmetadata of bestandsnaam. Bij mismatch → `NIET_CONTROLEERBAAR` met toelichting *"ECLI in Claim Register komt niet overeen met ECLI in bronbestand."*
- De regex-check is hier een tweede verdedigingslinie: een syntactisch ongeldige ECLI in het Claim Register kan nooit correct gekoppeld worden, markeer als `NIET_CONTROLEERBAAR`.
