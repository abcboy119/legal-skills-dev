# Agentic File Parsing
> Bijbehorende regel in `SKILL.md`: `<rules>` (Agentic File Parsing).

De gebruiker kan meerdere juridische documenten aanleveren op verschillende manieren. Deze referentie beschrijft hoe je ze identificeert, scheidt en labelt, zodat elke audit- en claim-identificatie (Claim_ID, Doc_ID) eenduidig terug te voeren is op één brondocument.

## 1. Voorkeursformaat: expliciete delimiters

Als de input expliciete delimiters bevat, gebruik deze dan zonder wijziging:

```xml
<document id="1">
... inhoud van document 1 ...
</document>
<document id="2">
... inhoud van document 2 ...
</document>
```

- Behoud de `id`-waarde exact zoals aangeleverd; gebruik deze als `Doc_ID` in het Claim Register (bijv. `Document 1`).
- Als de gebruiker geen `id`-attribuut geeft maar wel delimiters, ken dan opeenvolgende nummers toe (`Document 1`, `Document 2`, …) en vermeld dit kort in Stap 1.

## 2. Natuurlijke documentgrenzen (geen delimiters)

In de praktijk levert een gebruiker vaak één ongestructureerde tekst aan waarin meerdere documenten aan elkaar geplakt zijn. Herken documentgrenzen aan één of meer van de volgende signalen, in volgorde van betrouwbaarheid:

1. **Briefkop / afzenderblok** — een blok met naam, adres, datum, "Betreft:" markeert het begin van een nieuw document (bijv. bezwaarschrift, advies).
2. **Datumregel gevolgd door titel** — een geïsoleerde datumregel gevolgd door een korte titel ("Advies", "Bezwaarschrift", "Conclusie") is een sterke aanwijzing.
3. **Wisseling van documenttype-markering** — overgang van een memo-layout ("Van:/Aan:/Datum:") naar een brief-layout ("Geachte …") wijst op een nieuw document.
4. **Pagina-eindes** — `--- pagina X ---`, formfeed-tekens (`\f`), of duidelijke pagina-scheidingstekens.
5. **Sterke inhoudelijke breuk** — een plotselinge wissel van rechtsgebied, zaak, of partij, mét een van bovenstaande signalen.

### Procedure

- Markeer elke herkende grens expliciet met een interne notitie in Stap 1, bijv.: *"Gescheiden op basis van briefkop + datumregel tussen [posities X en Y]."*
- Ken opeenvolgende `Doc_ID`s toe (`Document 1`, `Document 2`, …).
- Als je **minder dan 80% zeker** bent van een grens, splits dan niet — behoud de tekst als één document en vermeld in Stap 1 dat er mogelijk meerdere documenten inzitten maar dat de grens onzeker was. Vraag de gebruiker om verduidelijking.

## 3. Bijlagen en meerdere bestanden

Als de gebruiker meerdere losse bestanden aanlevert (PDF, DOCX, JSON, XML, Markdown):

- Behandel elk bestand als één document, tenzij het bestand zelf meerdere documenten bevat (bijv. een PDF-bundel van meerdere bezwaarschriften).
- Bij een PDF/DOCX-bundel: probeer per sub-document een natuurlijke grens te herkennen (paginabreak + datum/afzender). Lukt dat niet, behandel de bundel dan als één document en vermeld dit.
- Converteer binaire formaten (PDF, DOCX) naar tekst vóór analyse. Als conversie faalt of de tekst onleesbaar is (OCR-rommel, base64-blobs), meld dit in Stap 1 en vraag om een leesbare versie.

## 4. Edge-cases

| Situatie | Actie |
|---|---|
| Één document met bijlagen die erin worden geciteerd | Eén `Doc_ID`; bijlagen apart vermelden in Stap 1 als "Genoemde bijlagen". |
| Meerdere documenten die naar dezelfde ECLI verwijzen | Eén `Doc_ID` per document; ECLI kan in meerdere Claim Register-rijen voorkomen met verschillende `Claim_ID`s. |
| Eén document gesplitst over meerdere berichten/uploads | Voeg de delen samen tot één `Doc_ID` vóór analyse; vermeld de samenvoeging in Stap 1. |
| Geen documenten aanwezig (lege input of alleen metadata) | Stop direct, meld "Geen juridische documenten aangetroffen", vraag om input. |
| Twijfel of een tekstblok een nieuw document is | Niet splitsen; vermeld de twijfel in Stap 1 en behoud als één document. |

## 5. Rapportage in Stap 1

Stap 1 (Documentoverzicht) moet altijd kort vermelden hoe documenten zijn geïdentificeerd en gescheiden. Voorbeeld:

> *"Aanlevering bevatte één ongestructureerde tekst zonder expliciete delimiters. Documenten gescheiden op basis van briefkoppen en datumregels. Drie documenten herkend: Document 1 (bezwaarschrift, datum 2024-03-12), Document 2 (advies, datum 2024-04-02), Document 3 (interne memo, ongedateerd)."*

Deze transparantie is essentieel omdat downstream fases (Fase 2, Fase 3) terugverwijzen naar `Doc_ID`. Een verkeerde splitsing halverwege corrigeren is duur; daarom rapporteer je de methode direct.
