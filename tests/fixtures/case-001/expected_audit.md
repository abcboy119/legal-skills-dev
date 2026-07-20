# Verwachte Fase 1 output — case-001

> Dit is de **verwachte** output van `documenten-audit` voor `tests/fixtures/case-001/input/docs.md`. Alleen de kritieke delen (Stap 1, Stap 9 Claim Register, Stap 10 manifest) zijn volledig uitgewerkt; Stap 2-8 zijn ingekort weergegeven omdat Fase 2 ze niet leest.

## Stap 1: Documentoverzicht

Aanlevering bevatte één ongestructureerde tekst met expliciete `<document id="1">` / `<document id="2">` delimiters. Twee documenten herkend op basis van delimiters.

| Document | Juridische vraag | Rechtsgebied | Kernantwoord | Bronnen | Documenttype |
|---|---|---|---|---|---|
| Document 1 | Is een dwangsom mogelijk bij niet-tijdige Woo-beantwoording? | bestuursrecht (Woo) | Ja, dwangsom mogelijk; rechtbank Den Haag kende €500/week toe. | ECLI:NL:RBDHA:2023:1234 | AI-advies |
| Document 2 | Wat is de Woo-termijn? | bestuursrecht (Woo) | Zes weken (niet vier), volgens Hoge Raad. | ECLI:NL:HR:23:1, ECLI:NL:HR:2022:9876 | Bezwaarschrift |

## Stap 2-5: [ingekort — thematische analyse, vergelijking, standpunten]

## Stap 6: Kwaliteitsscore per document (samengevat)

| Document | Duidelijkheid | Onderbouwing | Bronnen | Redenering | Uitzonderingen | Consistentie | Totaal |
|---|---|---|---|---|---|---|---|
| Document 1 | 4 | 4 | 4 | 4 | 2 | 4 | sterk |
| Document 2 | 3 | 2 | 2 | 2 | 1 | 2 | zwak |

Opmerking: Document 2 bevat een ECLI met ongeldig formaat (`ECLI:NL:HR:23:1`), wat de score op Bronnen negatief beïnvloedt.

## Stap 7-8: [ingekort — best onderbouwde antwoord, lacunes]

## Stap 9: Claim Register

| Claim_ID | Doc_ID | ECLI | Bewering | Extractie_Zekerheid | Opmerking |
|---|---|---|---|---|---|
| C001 | Document 1 | ECLI:NL:RBDHA:2023:1234 | Een dwangsom kan worden opgelegd bij niet-tijdige beantwoording van een Woo-verzoek. | HOOG | |
| C002 | Document 1 | N/A | Er is geen wettelijk maximum aan de op te leggen dwangsom. | MIDDEN | |
| C003 | Document 2 | ECLI:NL:HR:23:1 | De Woo-termijn bedraagt zes weken. | LAAG | ECLI voldoet niet aan formaat — vermoedelijke typfout of hallucinatie. |
| C004 | Document 2 | ECLI:NL:HR:2022:9876 | Een verlenging van de Woo-termijn met meer dan vier weken is onredelijk. | HOOG | |
| C005 | Document 2 | N/A | De overheid heeft in dit geval nalatig gehandeld. | LAAG | |

## Stap 10: Manifest Template

```json
{
  "ECLI:NL:RBDHA:2023:1234": "sources/ECLI_NL_RBDHA_2023_1234.json",
  "ECLI:NL:HR:2022:9876": "pad/naar/ECLI_NL_HR_2022_9876.json"
}
```

Opmerking: `ECLI:NL:HR:23:1` is niet opgenomen in het manifest omdat de ECLI niet aan de formaateis voldoet; een bronbestand kan niet betrouwbaar worden gekoppeld.
