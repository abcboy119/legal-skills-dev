# ECLI → volledige uitspraaktekst: wat bieden de officiële publieke kanalen (NL, EU, EHRM)?

**Datum:** 2026-08-14

**Onderwerp:** Welke volledige uitspraakteksten zijn momenteel via officiële, publieke kanalen te verkrijgen op basis van een ECLI, voor Nederlandse, EU- en EHRM-rechtspraak — en wat betekent dat voor het gat tussen Fase 1 (documenten-audit) en Fase 2 (ecli-verificatie) van de pijplijn?

## Waarom dit onderzoek bestaat

Fase 1 van de pijplijn (`documenten-audit`) produceert een manifest-template met de benodigde ECLI's, maar geen bronbestanden met de volledige uitspraakteksten. Fase 2 (`ecli-verificatie`) heeft die teksten nodig om beweringen in AI-gegenereerde juridische teksten tegen werkelijke uitspraken te verifiëren. De gebruiker moet die teksten nu handmatig aanleveren. Voor de ontwerpbeslissing of de distributie pure prompts blijft of een retrieval-stap nodig heeft (gedocumenteerde procedure, meegeleverd script of een vierde skill), is vastgesteld wat de officiële kanalen feitelijk bieden.

Alle bevindingen hieronder zijn geverifieerd tegen primaire bronnen (documentatie van de aanbieders zelf en/of live endpoints van de aanbieders), geraadpleegd op 2026-08-14. Waar iets niet kon worden vastgesteld, staat dat expliciet vermeld.

---

## 1. Nederland — Rechtspraak.nl Open Data

Open Data van de Rechtspraak is "de functionele vervanger van Dataleveranties Uitspraken (DUIT) en de LJN-webservice". Bron: https://www.rechtspraak.nl/Uitspraken/Paginas/Open-Data.aspx (geraadpleegd 2026-08-14).

### 1.1 Endpoint en responsformaat

De webservice bestaat uit twee gescheiden bevragingen (REST, XML). Bron: technische documentatie "Open Data van de Rechtspraak, Versie 1.15" (PDF), https://www.rechtspraak.nl/binaries/_rts_1768910542320/content/assets/ivo/wi/ivo-wi-technische-documentatie-open-data-van-de-rechtspraak.pdf (geraadpleegd 2026-08-14), en https://www.rechtspraak.nl/Uitspraken/Paginas/Open-Data.aspx (geraadpleegd 2026-08-14).

- **ECLI-index (metadata):** `https://data.rechtspraak.nl/uitspraken/zoeken` — retourneert een Atom-feed (XML). Gedocumenteerde parameters (technische documentatie v1.15, hfdst. 4): `instantie`, `type`, `date` (uitspraakdatum, met van/tot-bereik), `subject` (rechtsgebied), `modified` (wijzigingsdatum), `return` (waarde `DOC`: alleen ECLI's waarvan documenten beschikbaar zijn), `vervangen`, `max`, `from` (paginering; voorbeeld in de documentatie: `?modified=1995-01-01T12:00:00&max=500&from=501` retourneert entries 501 t/m 1000) en `sort` (ascending/descending). De feed kan via `deleted="doc"`/`deleted="ecli"`-attributen op entries aangeven dat documenten/ECLI's zijn verwijderd.
- **Uitspraakdocument:** `https://data.rechtspraak.nl/uitspraken/content?id=ECLI:...` — retourneert XML met: (a) RDF-metadata (identifier, instantie, uitspraakdatum, zaaknummer, type, procedure, rechtsgebied, formele relaties, vindplaatsen, enz.), (b) `<inhoudsindicatie>` (samenvatting) en (c) het element `<uitspraak>` (of `<conclusie>`) met **de volledige uitspraaktekst in gestructureerde XML** (`section`, `paragroup`, `para`, enz.; namespace `http://www.rechtspraak.nl/schema/rechtspraak-1.0`). Met `&return=META` wordt alleen de metadata geretourneerd. De documentatie formuleert letterlijk: "Retourneert zowel de metadata als het document **indien beschikbaar** voor de gevraagde ECLI". In het schema heeft het element `uitspraak | conclusie` cardinaliteit "0 of 1" — de tekst mag dus afwezig zijn.
- **Afbeeldingen:** `https://data.rechtspraak.nl/uitspraken/image?id=...`
- **HTML-weergave voor mensen:** de Atom-feed linkt naar `https://uitspraken.rechtspraak.nl/details?id=ECLI:...`.

Eigen verificatie via de live endpoints (2026-08-14):
- `https://data.rechtspraak.nl/uitspraken/zoeken?max=2` → Atom-feed met `<subtitle>Aantal gevonden ECLI's: 3742749</subtitle>`.
- `https://data.rechtspraak.nl/uitspraken/content?id=ECLI:NL:RBAMS:2023:3197` → metadata + `<inhoudsindicatie>` + `<uitspraak>` met volledige tekst.
- `https://data.rechtspraak.nl/uitspraken/content?id=ECLI:NL:RBARN:1998:AA1005` → metadata + volledige tekst (ook LJN-tijdperk-uitspraken met tekst werken).
- `https://data.rechtspraak.nl/uitspraken/content?id=ECLI:NL:XX:9999:1` (niet-bestaand) → HTTP 404.

### 1.2 Dekking en gaten (kernpunt)

- De ECLI-index bevatte op 14-08-2026 **3.742.749 ECLI's** (live teller in het `<subtitle>`-element van de Atom-feed, geraadpleegd 2026-08-14).
- Officiële datasetbeschrijving op data.overheid.nl (bijgewerkt 05-02-2026): "**Meer dan 800.000 uitspraken zijn beschikbaar. Van ruim 3 miljoen uitspraken zijn alleen de sleutelgegevens (ECLI-nummer, naam instantie, zaaknummer, datum uitspraak) en een evt. vindplaats opgenomen.**" Bron: https://data.overheid.nl/en/dataset/uitspraken-rechtspraak-nl (geraadpleegd 2026-08-14). Dat betekent dat ruwweg **4 op de 5 ECLI's in de index géén tekst heeft**.
- Eigen verificatie van het gedrag bij een ECLI zónder tekst: `content?id=ECLI:NL:HR:1913:1` retourneert **HTTP 200 met geldige XML die alleen de RDF-metadata bevat** (inclusief vindplaats "NJ 1913, p. 1034") — er is géén `<uitspraak>`- of `<inhoudsindicatie>`-element. Een consument die alleen op HTTP-status en well-formed XML controleert, "slaagt" dus met een lege bron.
- De technische documentatie bevestigt het bestaan van ECLI's zonder eigen tekst: "Uitspraken die op een vrij toegankelijk medium zijn gepubliceerd worden ook vermeld in de metadata ook al is de tekst niet op rechtspraak.nl beschikbaar. De enige andere bron op dit moment is tuchtrecht.overheid.nl" (technische documentatie v1.15, hfdst. 13).
- Temporele dekking volgens data.overheid.nl: "Gepubliceerde uitspraken vanaf 1999 / ECLI-register vanaf 1913" (https://data.overheid.nl/en/dataset/uitspraken-rechtspraak-nl, geraadpleegd 2026-08-14).
- De index biedt wel een filter om alleen ECLI's met document te selecteren: `return=DOC` (technische documentatie v1.15, hfdst. 4.3.6).

### 1.3 Gebruiksvoorwaarden en limieten

- De webservice is "een **kosteloze en publieke** dienst". Limieten volgens de Open Data-pagina: "Het aantal toegestane informatieverzoeken is gelimiteerd. Het is **niet mogelijk een complete set te downloaden** en het is **niet mogelijk meer dan 10 requests/calls per seconde** in te dienen." Bron: https://www.rechtspraak.nl/Uitspraken/Paginas/Open-Data.aspx (geraadpleegd 2026-08-14).
- "**Er wordt momenteel geen ondersteuning geboden** op het aansluiten en het gebruik van de webservice." Bron: idem.
- Licentie: de dataset staat op data.overheid.nl geregistreerd met licentietype **"Publiek domein" (CC-0 1.0)**, distributie "XML CC-0 (1.0)" en "RSS CC-0 (1.0)". Bron: https://data.overheid.nl/en/dataset/uitspraken-rechtspraak-nl (geraadpleegd 2026-08-14). Opmerkelijk detail: de Atom-feed zelf vermeldt `<rights>Copyright 2026 Rechtspraak.</rights>` (live respons, 2026-08-14) — dat staat naast de CC0-registratie op data.overheid.nl; wat juridisch leidend is, is uit de primaire bronnen niet op te maken.
- Geen authenticatie of registratie vereist (eigen verificatie via live endpoints, 2026-08-14).

### 1.4 Stabiliteit

- Open Data is expliciet de opvolger van twee afgeschafte diensten: "Open Data van de Rechtspraak is de functionele vervanger van Dataleveranties Uitspraken (DUIT) en de LJN-webservice." Bron: https://www.rechtspraak.nl/Uitspraken/Paginas/Open-Data.aspx (geraadpleegd 2026-08-14).
- De technische documentatie draagt een versienummer: **v1.15** (PDF, gegenereerd circa januari 2026 op basis van de asset-timestamp in de URL). Bron: https://www.rechtspraak.nl/binaries/_rts_1768910542320/content/assets/ivo/wi/ivo-wi-technische-documentatie-open-data-van-de-rechtspraak.pdf (geraadpleegd 2026-08-14).
- Signaal van onderhoudsachterstand: de link naar de "Schemabestanden (ZIP)" op de officiële Open Data-pagina verwijst inmiddels naar een **archiefkopie** (`archief07.archiefweb.eu`) in plaats van een live bestand. Bron: https://www.rechtspraak.nl/Uitspraken/Paginas/Open-Data.aspx (geraadpleegd 2026-08-14).
- De HTML-weergave is gemigreerd naar `uitspraken.rechtspraak.nl/details?id=...` (de Atom-feed verwijst hiernaar; geraadpleegd 2026-08-14). Er is geen officiële deprecatie-aankondiging van de Open Data-endpoints aangetroffen.

---

## 2. EU — EUR-Lex / CURIA

### 2.1 Endpoint en responsformaat

**EUR-Lex (Publicatiebureau) — het feitelijke tekstkanaal voor HvJ-jurisprudentie:**

- **ECLI-URL's zijn officieel gedocumenteerd als permanente links.** Bron: https://eur-lex.europa.eu/content/help/data-reuse/linking.html (geraadpleegd 2026-08-14):
  - Tekstweergave: `https://eur-lex.europa.eu/legal-content/{TAAL}/TXT/?uri=ecli:ECLI:EU:C:2016:718`
  - HTML-weergave: `.../TXT/HTML/?uri=ecli:ECLI:EU:C:2016:718`
  - XML-notice: `.../TXT/XML/?uri=ecli:ECLI:EU:F:2016:177`
- Eigen verificatie (2026-08-14): `https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=ecli:ECLI:EU:C:2016:718` retourneert **de volledige uitspraaktekst** ("BREITSAMER UND ULRICH, JUDGMENT OF THE COURT (Third Chamber)…"). De XML-notice bij dezelfde ECLI bevat metadata én per taal verwijzingen naar manifestaties (xhtml, fmx4, pdfa1a, txt, xml), met per taalversie een eigen `ECLI:...LANG`-URI. De volledige tekst zit dus niet ín de notice, maar is via de gedocumenteerde URL's en manifestaties op te halen.
- **EUR-Lex webservice (SOAP):** geregistreerde gebruikers kunnen EUR-Lex direct bevragen; levert XML; "Although the webservice allows you to search within the text of the documents themselves, it **cannot be used to directly download the document files**. You can download these based on their identifier, either via the **Cellar RESTful API** or by creating a URL as described in our guidelines for stable links." Bron: https://eur-lex.europa.eu/content/help/data-reuse/webservice.html (geraadpleegd 2026-08-14).
- **CELLAR (Publicatiebureau):** het onderliggende data-repository van EUR-Lex. Officiële interfaces: HTTP RESTful webservices voor publicaties en metadata-notices, een SPARQL-interface op de knowledge graph, en RSS/Atom-feeds. Bron: https://op.europa.eu/en/web/cellar/cellar-data (geraadpleegd 2026-08-14). Het SPARQL-endpoint: `http://publications.europa.eu/webapi/rdf/sparql` (genoemd als "Direct access to the CELLAR API" op https://eur-lex.europa.eu/content/help/data-reuse/webservice.html, geraadpleegd 2026-08-14). Voor grote volumes verwijst EUR-Lex naar de **Data Dump**-dienst: https://datadump.publications.europa.eu/create-download-request (idem).

**CURIA (het Hof zelf):**

- CURIA biedt de jurisprudentiedatabank/zoekmachine **InfoCuria** (in 2025-2026 vernieuwd; "new InfoCuria case-law database and search tool"). Bron: https://curia.europa.eu/site/jcms/p1_1000063986/en/new-infocuria-case-law-database-and-search-tool (geraadpleegd 2026-08-14).
- Het zoekformulier van CURIA (https://juris.curia.europa.eu/juris/recherche.jsf?language=en, "last update 24/06/2026", geraadpleegd 2026-08-14) heeft een **ECLI-zoekcriterium**; resultaten linken voor de tekst door naar EUR-Lex (bijv. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62026TO0267, gezien op https://infocuria.curia.europa.eu/, geraadpleegd 2026-08-14).

### 2.2 Dekking en gaten

- Officiële CURIA-pagina "Case names and citations": "The Court has assigned an ECLI to **all decisions delivered by the EU courts since 1954**, including Advocate General Opinions." Bron: https://curia.europa.eu/site/jcms/d2_5132/en/case-names-and-citations (geraadpleegd 2026-08-14). Er is dus géén periode-gat in ECLI-toekenning voor EU-rechtspraak.
- De tekstdekking op EUR-Lex is per zaak meertalig: per taaluitgave bestaat een aparte expression/manifestation (XML-notice van ECLI:EU:C:2016:718 toont o.a. LAV en DEU edities; eigen verificatie 2026-08-14).
- Europeserechtelijk authenticiteitsvoorbehoud: "With respect to case-law, only the versions of documents published in the 'European Court Reports' are deemed official sources." Bron: https://eur-lex.europa.eu/content/legal-notice/legal-notice.html (geraadpleegd 2026-08-14).
- Open punt dat wél uit primaire bron blijkt: op de EUR-Lex case-law-pagina staat dat zoeken op subject matter in overgang is en dat beslissingen **na 20 juni 2025 tijdelijk niet vindbaar zijn op subject matter** ("decisions delivered after 20 June 2025 will temporarily not be retrievable when searching by subject matter"). Bron: https://eur-lex.europa.eu/collection/eu-law/eu-case-law.html (geraadpleegd 2026-08-14). Dit raakt zoeken op onderwerp, niet de ECLI-opvraag zelf.

### 2.3 Gebruiksvoorwaarden en limieten

- **EUR-Lex webservice:** gratis, maar **registratie vereist** (EU Login + goedkeuring door de beheerder; in het aanmeldformulier wordt gevraagd naar "Maximum number of calls per day"). Limieten per dag zijn instelbaar/onderhandelbaar; "The maximum daily number of calls to the webservice is limited." Bron: https://eur-lex.europa.eu/content/help/data-reuse/webservice.html (geraadpleegd 2026-08-14).
- **Per 1 januari 2026: maximaal 10.000 resultaten per zoekopdracht** via de webservice, met verwijzing naar https://eur-lex.europa.eu/content/tools/webservice-limit.pdf en voor grote volumes naar de CELLAR-API of de Data Dump. Bron: https://eur-lex.europa.eu/content/help/data-reuse/webservice.html (geraadpleegd 2026-08-14).
- **Hergebruik:** "Unless otherwise specified, you can re-use the legal documents published in EUR-Lex for **commercial or non-commercial purposes**" (Commissie-hergebruiksbeleid, Besluit 2011/833/EU). Editorial content/samenvattingen/geconsolideerde teksten: **CC-BY 4.0**; EUR-Lex **metadata: CC0 1.0**. Bron: https://eur-lex.europa.eu/content/legal-notice/legal-notice.html (geraadpleegd 2026-08-14).
- Over expliciete rate limits voor de (ongeauthenticeerde) `legal-content`-URL's of het CELLAR SPARQL-endpoint is geen publieke primaire documentatie aangetroffen (zie §5).

### 2.4 Stabiliteit

- De ECLI-URL-structuur wordt gepresenteerd als "permanent/stable link" met garantie van blijvende toegang. Bron: https://eur-lex.europa.eu/content/help/data-reuse/linking.html (geraadpleegd 2026-08-14).
- CELLAR wordt actief doorontwikkeld met genummerde releases ("The new Cellar release 8.15.0 has been installed! The new CDM release 4.16.1 has been installed!"). Bron: https://op.europa.eu/en/web/cellar (geraadpleegd 2026-08-14).
- EUR-Lex zelf kondigt gewijzigde limieten aan (10.000-resultaatlimiet vanaf 1-1-2026, hierboven) — dat is een recente, officieel aangekondigde wijziging.
- CURIA: het vernieuwde InfoCuria is recent gelanceerd en "will be constantly updated"; een geavanceerde zoekinterface voor juristen is aangekondigd ("under development and will be launched soon"). Bron: https://curia.europa.eu/site/jcms/p1_1000063986/en/new-infocuria-case-law-database-and-search-tool (geraadpleegd 2026-08-14). Over de oude `juris.curia.europa.eu`-zoekinterface is geen deprecatie-aankondiging gevonden; beide bestaan naast elkaar (beide geraadpleegd 2026-08-14).

---

## 3. EHRM — HUDOC

### 3.1 Endpoint en responsformaat

- **Officiële, gedocumenteerde kanalen:** HUDOC is de jurisprudentiedatabank van het EHRM (https://hudoc.echr.coe.int/). De officiële documentatie bestaat uit een **User Manual en FAQ** (verwijzing op https://www.echr.coe.int/hudoc-database, geraadpleegd 2026-08-14; de PDF's zelf retourneerden 403 bij raadpleging, zie §5). De zoekinterface zelf heeft een **ECLI-veld** in de geavanceerde zoekopdracht (live zoekformulier https://hudoc.echr.coe.int/eng, geraadpleegd 2026-08-14).
- **Feitelijk werkende machine-interfaces (live geverifieerd 2026-08-14, maar niet in officiële publieke documentatie teruggevonden):**
  - Zoeken (JSON): `https://hudoc.echr.coe.int/app/query/results?query=contentsitename:ECHR AND doctype=HEJUD&select=itemid,docname,ecli&sort=kpdate Descending&start=0&length=2` → retourneert JSON met `resultcount`, `itemid`, `docname` en **`ecli`** per resultaat (bijv. `ECLI:CE:ECHR:2026:0723JUD002446523`).
  - Volledige tekst (HTML): `https://hudoc.echr.coe.int/app/conversion/docx/html/body?library=ECHR&id=001-251251` → retourneert de **volledige uitspraaktekst** als HTML.
- Exportfuncties in de UI: CSV en Excel, met de opmerking "Only a maximum of 2000 results can be exported", plus RSS-feed per zoekresultaat. Bron: live zoekinterface https://hudoc.echr.coe.int/eng (geraadpleegd 2026-08-14).

### 3.2 Dekking en gaten

- Inhoud van HUDOC (officiële beschrijving): jurisprudentie van het Hof (Grand Chamber-, Chamber- en Committee-arresten en -beslissingen, communicated cases, adviesopinies en legal summaries), de voormalige Europese Commissie voor de Rechten van de Mens (beslissingen en rapporten) en resoluties van het Comité van Ministers. Bron: https://www.echr.coe.int/hudoc-database (geraadpleegd 2026-08-14).
- Officieel benoemde gaten (zelfde bron): "Committee decisions appeared on HUDOC **only as of April 2010**. **Decisions concerning single judge cases are not published.** Commission decisions **prior to 1960** exist in hard copy only in the Court Archives."
- **ECLI-dekking:** EHRM-uitspraken dragen ECLI's van de vorm `ECLI:CE:ECHR:...`. Eigen verificatie (2026-08-14): zelfs het oudste arrest (Lawless v. Ireland (No. 1), 1960) heeft een ECLI (`ECLI:CE:ECHR:1960:1114JUD000033257`), dus ECLI's zijn (ten minste voor Engelstalige judgments) met terugwerkende kracht toegekend. De API-query voor `doctype=HEJUD` (Engelstalige judgments) gaf op 14-08-2026 `resultcount: 29213`. Een officiële primaire bron die de retroactieve ECLI-toekenning door het EHRM expliciet beschrijft (analoog aan de CURIA-pagina) is **niet** gevonden (zie §5).

### 3.3 Gebruiksvoorwaarden en limieten

- HUDOC is vrij toegankelijk zonder registratie (eigen verificatie, 2026-08-14).
- Exportlimiet: maximaal 2000 resultaten per export in de UI (live zoekinterface, geraadpleegd 2026-08-14).
- **Niet kunnen vaststellen:** officiële gebruiksvoorwaarden/rate limits voor de machine-interfaces. De relevante pagina's op echr.coe.int en coe.int (FAQ-PDF, copyright-pagina) retourneerden 403 bij raadpleging op 2026-08-14, en publieke API-documentatie met limieten is niet aangetroffen. Zie §5.

### 3.4 Stabiliteit

- De JSON- en tekst-endpoints van HUDOC (`/app/query/results`, `/app/conversion/docx/html/body`) zijn interne interfaces zonder versienummering of publieke documentatie; hun stabiliteit is formeel niet gegarandeerd — dit valt onder de open vragen (§5).
- De UI biedt gedocumenteerde stabiele permalinks per document van de vorm `https://hudoc.echr.coe.int/eng?i=001-...` (zichbaar in zoekresultaten; geraadpleegd 2026-08-14).
- Geen deprecatie-aankondigingen aangetroffen.

---

## 4. Synthese: wat betekent dit voor het gat tussen Fase 1 en Fase 2?

1. **NL: tekst ophalen kán officieel en programmatisch, maar alleen voor een minderheid van de ECLI's.** Het `content`-endpoint levert volledige tekst in gestructureerde XML voor ruwweg 800.000+ uitspraken, tegenover ruim 3 miljoen ECLI's die alleen metadata hebben (data.overheid.nl, 05-02-2026; index-teller 3,74M op 14-08-2026). De uitdaging is niet het ophalen, maar het **detecteren van het gat**: een metadata-only ECLI geeft HTTP 200 met geldige XML zónder `<uitspraak>`-element, terwijl een onbekende ECLI een HTTP 404 geeft. De schema-cardinaliteit "0 of 1" voor `uitspraak|conclusie` maakt dit een formeel gedocumenteerde eigenschap van het format, niet een fout. Voor het Claim Register betekent dat: een lege bron is stil, en "bron opgehaald" ≠ "bron heeft tekst".
2. **EU: tekst ophalen per ECLI is officieel en vrijwel dekkend.** EUR-Lex documenteert ECLI-permalinks (`legal-content/.../TXT(HTML/XML)/?uri=ecli:...`), CURIA bevestigt ECLI's voor alle beslissingen sinds 1954, en de volledige tekst is per taaluitgave op te halen (live geverifieerd). Beperkingen: de SOAP-webservice vereist registratie en is per 1-1-2026 gemaximeerd op 10.000 resultaten per zoekopdracht; ongeauthenticeerde document-URL's zijn voor het ophalen per ECLI echter voldoende. Voor bulk geldt CELLAR/SPARQL of de Data Dump.
3. **EHRM: tekst ophalen per ECLI werkt feitelijk, maar niet officieel.** HUDOC draagt ECLI's (zelfs retroactief tot 1960, live geverifieerd) en er zijn werkende machine-endpoints voor zoeken (JSON, mét `ecli`-veld) en volledige tekst (HTML), maar deze zijn **niet** terug te vinden in officiële publieke documentatie. Het zoeken óp ECLI via die endpoints kon niet worden gereproduceerd (de query-syntax van het ECLI-veld kon niet worden vastgesteld); de UI heeft het ECLI-veld wél. Inhoudelijke gaten zijn officieel benoemd: single-judge decisions worden niet gepubliceerd, Committee-beslissingen pas vanaf april 2010 in HUDOC.
4. **Voor de pijplijn als geheel:** de drie kanalen zijn asymmetrisch — NL is tekstarm (ca. 1 op 5 ECLI's heeft tekst), EU is tekstrijk, EHRM is tekstrijk maar ongedocumenteerd qua machine-toegang. Een retrieval-stap die voor elk kanaal hetzelfde "succes"-criterium hanteert (HTTP 200) zou in het NL-kanaal structureel lege bronnen als vol beschouwen. Omgekeerd biedt elk kanaal wél een officieel, controleerbaar signaal om een lege bron te herkennen: NL heeft `return=DOC` in de index en de aanwezigheid van het `<uitspraak>`-element; EUR-Lex en HUDOC hebben per document een expliciete tekstmanifestatie. Dat maakt een "bron zonder tekst"-toestand in principe detecteerbaar en rapporteerbaar, in plaats van stilletjes leeg.

---

## 5. Niet kunnen vaststellen / open vragen

1. **Rechtspraak Open Data — volledige parameter-/limietdetails buiten de website.** De maximale paginagrootte (`max`) en eventuele HTTP-foutcodes zijn weliswaar beschreven in de technische documentatie v1.15, maar die PDF bleek bij extractie gedeeltelijk onleesbaar (binaire tabelvelden); alleen de hierboven geciteerde parameters zijn geverifieerd. Een volledige opsomming van foutmeldingen (hfdst. 4.5) kon niet tekstueel worden hersteld.
2. **Rechtspraak — welke ECLI's precies géén tekst hebben.** Het totale aandeel (ca. 800k mét tekst vs. ruim 3M zonder) komt uit de datasetbeschrijving van data.overheid.nl (bijgewerkt 05-02-2026); een actuelere uitsplitsing per jaar of instantie is niet gepubliceerd. Ook is niet officieel gedocumenteerd hóé bepaald wordt dat een uitspraak alleen metadata krijgt.
3. **Rechtspraak — juridische status van de CC0-licentie vs. de "Copyright 2026 Rechtspraak"-regel in de Atom-feed.** Beide komen uit primaire bronnen maar spreken elkaar ogenschijnlijk tegen; geen primaire bron gevonden die dit expliciet beslecht.
4. **EUR-Lex — rate limits voor de ongeauthenticeerde document-URL's en het CELLAR SPARQL-endpoint.** Alleen de webservice-limieten (registratie, daglimiet, 10.000 resultaten vanaf 1-1-2026) zijn officieel gedocumenteerd; voor de overige interfaces is geen publieke limietdocumentatie gevonden.
5. **CURIA — officiële API.** Op curia.europa.eu is géén publieke API-documentatie aangetroffen; CURIA biedt (voor zover vastgesteld) alleen de webzoekinterface, met tekstlevering via EUR-Lex. Of er een ongedocumenteerde machine-interface bestaat, is niet vastgesteld. (Opmerkingen van derden dat er "geen publieke API" is, zijn bewust niet als feit overgenomen omdat ze niet-primair zijn.)
6. **EHRM — officiële documentatie van de machine-endpoints.** De JSON-zoekendpoint en het HTML-tekstendpoint zijn live geverifieerd, maar komen niet voor in officiële publieke documentatie; hun ondersteuningsstatus, versiebeleid en rate limits zijn onbekend. De HUDOC FAQ/User Manual-PDF's gaven 403 bij raadpleging (botblokkering op echr.coe.int).
7. **EHRM — zoeksyntax van het ECLI-veld in de machine-interface.** De UI heeft een ECLI-veld, maar het is niet gelukt de bijbehorende querysyntax voor het JSON-endpoint te reproduceren (proeven met `ecli=...` en tekst-zoekopdrachten gaven 404).
8. **EHRM — officiële bron over retroactieve ECLI-toekenning.** Dat ECLI's teruggaan tot 1960 is live vastgesteld, maar een officiële EHRM-pagina die dit beleid beschrijft is niet gevonden. Ook de reikwijdte (alleen judgments of ook decisions/vertalingen) is daarmee niet officieel bevestigd.
9. **EHRM — gebruiksvoorwaarden en hergebruik.** De officiële voorwaardenpagina's waren niet bereikbaar (403); niet vastgesteld onder welke voorwaarden HUDOC-teksten (her)gebruikt mogen worden.

---

## Bronnenoverzicht (alle geraadpleegd op 2026-08-14)

| Bron | URL |
|---|---|
| Rechtspraak — Open Data-pagina | https://www.rechtspraak.nl/Uitspraken/Paginas/Open-Data.aspx |
| Rechtspraak — Technische documentatie Open Data v1.15 (PDF) | https://www.rechtspraak.nl/binaries/_rts_1768910542320/content/assets/ivo/wi/ivo-wi-technische-documentatie-open-data-van-de-rechtspraak.pdf |
| Rechtspraak — live endpoints (eigen verificatie) | https://data.rechtspraak.nl/uitspraken/zoeken , https://data.rechtspraak.nl/uitspraken/content |
| data.overheid.nl — dataset "Uitspraken rechtspraak.nl" (bijgewerkt 05-02-2026) | https://data.overheid.nl/en/dataset/uitspraken-rechtspraak-nl |
| EUR-Lex — Webservice-hulp | https://eur-lex.europa.eu/content/help/data-reuse/webservice.html |
| EUR-Lex — Permanente links (ECLI) | https://eur-lex.europa.eu/content/help/data-reuse/linking.html |
| EUR-Lex — ECLI-hulp | https://eur-lex.europa.eu/content/help/eurlex-content/ecli.html |
| EUR-Lex — Legal notice (hergebruik) | https://eur-lex.europa.eu/content/legal-notice/legal-notice.html |
| EUR-Lex — EU case-law-collectie | https://eur-lex.europa.eu/collection/eu-law/eu-case-law.html |
| EUR-Lex — live ECLI-opvraag (eigen verificatie) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=ecli:ECLI:EU:C:2016:718 en .../EN/TXT/XML/?uri=ecli:ECLI:EU:C:2016:718 |
| Publicatiebureau — Cellar (homepage en data-pagina) | https://op.europa.eu/en/web/cellar , https://op.europa.eu/en/web/cellar/cellar-data |
| CURIA — Case names and citations (ECLI sinds 1954) | https://curia.europa.eu/site/jcms/d2_5132/en/case-names-and-citations |
| CURIA — Aankondiging nieuw InfoCuria | https://curia.europa.eu/site/jcms/p1_1000063986/en/new-infocuria-case-law-database-and-search-tool |
| CURIA — zoekformulier (ECLI-criterium, "last update 24/06/2026") | https://juris.curia.europa.eu/juris/recherche.jsf?language=en |
| InfoCuria — homepage | https://infocuria.curia.europa.eu/ |
| e-justice — ECLI-pagina (zoekmachine + resolver) | https://e-justice.europa.eu/topics/legislation-and-case-law/european-case-law-identifier-ecli_en |
| EHRM — HUDOC-databasebeschrijving | https://www.echr.coe.int/hudoc-database |
| HUDOC — zoekinterface (ECLI-veld, exportlimiet) | https://hudoc.echr.coe.int/eng |
| HUDOC — live endpoints (eigen verificatie) | https://hudoc.echr.coe.int/app/query/results , https://hudoc.echr.coe.int/app/conversion/docx/html/body |
