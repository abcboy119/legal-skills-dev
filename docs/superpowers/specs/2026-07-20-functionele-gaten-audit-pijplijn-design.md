# Design: functionele gaten in de audit-pijplijn dichten

**Status:** geïmplementeerd (versies 2.1.0/2.1.0/1.1.0 — zie CHANGELOG.md)
**Datum:** 2026-07-20
**Betrokken skills:** `documenten-audit` (2.0.0 → 2.1.0), `ecli-verificatie` (2.0.0 → 2.1.0), `audit-synthese` (1.0.0 → 1.1.0)

## Context en doel

Een eerdere reviewronde (zie git-historie, commits t/m `385ac82`/`c89a73f` op branch `claude-skill`) richtte zich op **structurele consistentie**: schema-mismatches, kapotte cross-file-verwijzingen, een validator-gat, typo's. Die punten zijn opgelost.

Deze ronde stelt een andere vraag: **kan een jurist de drie skills nu daadwerkelijk op echte documenten loslaten, zonder dat er iets essentieels ontbreekt in de workflow zelf?** Dat leverde zeven functionele gaten op (zie hieronder), onderverdeeld in "blokkerend voor echt gebruik" en "belangrijk maar niet blokkerend". Alle zeven zijn in scope voor dit ontwerp; drie ervan (punt 6 en 7, en deels punt 2) zijn direct geïnformeerd door een bestaande, losstaande Python-toolkit (`/home/badr/Claude/Projects/Open Data Rechtspraak/`) die al precies het databodel spreekt dat de pijplijn verwacht.

**Niet in scope voor deze ronde** (bewust uitgesteld, zie eerdere conversatie): PII/persoonsgegevens-richtlijn, round-trip-mechanisme na Fase 3-correcties, live ECLI-zoekhulp via `rechtspraak_client.py`'s zoekfunctie.

## Gevonden toolkit: `/home/badr/Claude/Projects/Open Data Rechtspraak/`

Vier relevante scripts, extern aan deze repo, niet te wijzigen als onderdeel van dit ontwerp:

| Script | Doel | Relevantie |
|---|---|---|
| `ecli_lookup_V10.py` | Batchgewijs NL/EU/EHRM-uitspraken ophalen voor een bekende ECLI-lijst → normalized JSON | Output-contract is vrijwel identiek aan wat `ecli-verificatie` verwacht (`tekst_waarschuwing` met exact `LEGE_TEKST`/`KORTE_TEKST`, velden `instantie`/`datum`/`rechtsgebied`) |
| `rechtspraak_client.py` | Zoeken naar ECLI's op metadata (NL only) | Niet in scope nu — mogelijk basis voor een latere "ECLI-zoekhulp"-uitbreiding |
| `ecli_zoek_soortgelijk.py` | Verwante zaken vinden via citatie-analyse (NL only, hardcoded voor één casus) | Niet in scope nu |
| `ECLI scanner/ecli_scanner.py` | Documenten (PDF/DOCX/ODT/RTF/TXT/MD) scannen op ECLI-vermeldingen, optioneel live-valideren tegen rechtspraak.nl | Deterministische cross-check op Fase 1's Stap 9 (ECLI-extractie) |

Geconstateerde kwaliteitspunten in `ecli_lookup_V10.py` (niet dit ontwerp se, maar relevant voor betrouwbaarheid van punt 6): placeholder-mailadres in `USER_AGENT`, gedupliceerde `RateLimiter`-implementatie t.o.v. `rechtspraak_client.py`, module-globals die hergebruik als bibliotheek bemoeilijken, `README.md`'s eigen Snelstart verwijst naar ontbrekende `requirements.txt`/`voorbeeld.py`. Deze repo's `docs/workflow.md` zal dit script als **extern, ongewijzigd** hulpmiddel documenteren — bovenstaande punten zijn dus geen actiepunt van dít ontwerp, maar het is goed dat ze vastliggen mocht die toolkit zelf ooit worden opgeschoond.

## De zeven punten

### 1. Foutafhandeling bij kapotte input (Fase 2/3) — Hoog

**Probleem:** Fase 2 gaat er blind van uit dat er een geldig Claim Register in het aangeleverde Markdown-bestand staat; Fase 3 gaat er blind van uit dat de JSON aan het 16-velden-schema voldoet. Geen van beide heeft een expliciete "stop en vraag om verduidelijking"-instructie zoals Fase 1's `<scope>` die al wel heeft voor "geen juridische inhoud".

**Wijzigingen:**
- `skills/ecli-verificatie/SKILL.md` (`<source_handling>`) en `references/source-handling.md`: regel toevoegen — geen herkenbaar Claim Register (tabel met kolommen Claim_ID/Doc_ID/ECLI/Bewering/Extractie_Zekerheid) → stop, meld dit expliciet, ga niet door met giswerk.
- `skills/audit-synthese/SKILL.md` (`<rules>`): regel toevoegen — JSON niet parseerbaar, of mist verplichte velden uit `output.schema.json` → stop, meld welke velden ontbreken/afwijken.

### 2. Context-budget-strategie voor Fase 1 — Hoog

**Probleem:** Fase 2 heeft een volledige `context-budget.md` (chunking, verificatievolgorde, overflow-signalen). Fase 1 heeft niets vergelijkbaars, terwijl een realistisch dossier van 15-20 documenten (of een paar zeer lange stukken) tegen hetzelfde probleem aanloopt.

**Wijziging:**
- Nieuw: `skills/documenten-audit/references/context-budget.md`. **Eigen strategie, geen kopie van Fase 2's aanpak** — Fase 1's probleem is "veel/lange brondocumenten auditen en vergelijken", niet "één lange uitspraak tegen veel claims verifiëren". Inhoud: batchgewijs documenten verwerken (bijv. groepen van ~5, of op geschat tokenbudget), per batch een deel-Claim-Register produceren, aan het eind consolideren zonder Claim_ID-botsingen (doorlopende nummering over batches heen), signalen van overflow specifiek voor multi-documentvergelijking.
- Pointer in `documenten-audit/SKILL.md` (`<rules>` of nieuwe sectie).

### 3. Bulk-modus testdekking — Hoog

**Probleem:** `ecli-verificatie/references/context-budget.md` §4 beschrijft expliciet hoe je meerdere claims per ECLI afhandelt (tot 10 per sessie, batchen daarboven), maar de enige worked example (`case-001`) heeft toevallig steeds precies één claim per ECLI. Nooit getest.

**Wijziging:**
- Nieuwe fixture `tests/fixtures/case-002/`: minstens twee claims gekoppeld aan dezelfde ECLI, met verwachte output die §4's bulk-modus-gedrag aantoont (waaronder de "Zie ook C00X voor context"-toelichting).
- Nieuwe test-functie(s) in `tests/test_pipeline_contracts.py` die deze fixture valideert.

### 4. Eén ECLI per claim — Midden

**Probleem:** Het Claim Register-schema staat maar één ECLI-kolom per rij toe. Een bewering onderbouwd door "vaste rechtspraak" (meerdere uitspraken) heeft geen modelleerwijze.

**Gekozen aanpak (A — conventie, geen schema-wijziging):** een bewering met meerdere ondersteunende ECLI's krijgt meerdere Claim Register-rijen (zelfde `Bewering`-tekst, verschillende `Claim_ID` en `ECLI`), gelinkt via een nieuwe optionele kolom.

**Wijzigingen:**
- `documenten-audit/references/claim-register-schema.md`: nieuwe optionele kolom `Gerelateerde_Claims` (bijv. "C005, C006"), conventie uitgeschreven.
- `documenten-audit/assets/claim-register-template.md`: voorbeeldrij(en) die dit demonstreren.
- Geen wijziging aan `output.schema.json` of aan Fase 2/3 — elke rij blijft één zelfstandige verificatie-eenheid.

### 5. Jurisdictie buiten NL/EU/EHRM — Midden

**Probleem:** de ECLI-regex accepteert elke geldige ECLI-vorm (dus ook bijv. Duitse of Franse nationale ECLI's), maar `jurisdiction-hierarchy.md` dekt uitsluitend NL/EU/EHRM. Geen instructie voor wat er met een ECLI buiten die scope moet gebeuren.

**Gekozen aanpak:** expliciet markeren als buiten scope, niet stilzwijgend proberen te verifiëren volgens regels die er niet op van toepassing zijn (in lijn met de bestaande mensen-in-de-loop-filosofie).

**Wijzigingen:**
- `documenten-audit/references/jurisdiction-hierarchy.md`: nieuwe sectie "Jurisdicties buiten deze distributie" — welke ECLI-prefixen (landcode ≠ NL, EU, CE) hieronder vallen en hoe dat te signaleren in Fase 1.
- `ecli-verificatie/references/source-handling.md`: regel — ECLI-prefix buiten NL/EU/CE(EHRM) → oordeel `NIET_CONTROLEERBAAR` met toelichting "buiten scope van deze distributie (jurisdiction: NL,EU,EHRM)".

### 6. Brug naar `ecli_lookup_V10.py` — Midden

**Probleem:** Fase 1's Stap 10 (Manifest Template) levert `{"ECLI:...": "pad/naar/bronbestand.json"}` — de gebruiker moet zelf bronbestanden vinden en aanleveren vóór Fase 2 kan draaien. Er bestaat al een extern, werkend script dat dit doet en zelfs (grotendeels toevallig) hetzelfde datacontract spreekt, maar dat is nergens gedocumenteerd.

**Wijzigingen (documentatie-only, geen wijziging aan het externe script):**
- `docs/workflow.md`: nieuwe (sub)sectie die de optionele handmatige tussenstap beschrijft: (a) ECLI-keys uit Fase 1's manifest naar een platte `eclis.txt` (één per regel) omzetten — het script verwacht dat formaat, niet de JSON-vorm; (b) het script draaien; (c) de output — ofwel de individuele `*.normalized.json`-bestanden, ofwel het script's eigen rijkere `ecli-manifest-v1`-manifest — rechtstreeks als Fase 2-input gebruiken.
- `ecli-verificatie/references/source-handling.md`: vermelden dat een aangeleverd manifest ook in de `ecli-manifest-v1`-vorm kan binnenkomen (met `items`-array i.p.v. platte key-value-mapping), en hoe daarmee om te gaan.

### 7. `ecli_scanner.py` als cross-check — Midden

**Probleem:** Fase 1's ECLI-extractie (Stap 9) gebeurt volledig door het LLM, zonder enige cross-check. Twee risico's blijven ongedekt: het LLM **mist** een ECLI die wél in de tekst staat, of het LLM **verzint** een ECLI die niet in de brontekst voorkomt.

**Wijziging (optionele stap, geen verplichting):**
- Nieuw: `documenten-audit/references/ecli-scanner-crosscheck.md` — beschrijft de optionele stap: `ecli_scanner.py` los over dezelfde brondocumenten draaien vóór/naast Stap 9, de output als ground-truth-lijst naast de LLM-extractie leggen.
  - ECLI door het LLM geëxtraheerd maar niet in de scanner-lijst → extra scrutinize, `Extractie_Zekerheid = LAAG` met opmerking "niet bevestigd door deterministische scan — mogelijke hallucinatie."
  - ECLI in de scanner-lijst maar niet als claim opgenomen → signaleren voor menselijke controle in Stap 8 (Lacunes), niet automatisch toevoegen (niet elke vermelding is een dragende claim).
- Pointer in `documenten-audit/SKILL.md` Stap 9, expliciet gemarkeerd als **optioneel** (scanner is een extern hulpmiddel, niet altijd beschikbaar of gewenst).

## Versiebeleid

Volgens `docs/conventions.md` §7 zijn dit allemaal additieve wijzigingen (nieuwe optionele velden/kolommen, nieuwe reference-docs, nieuwe regels die alleen ingrijpen bij eerder ongedefinieerd gedrag) — geen breaking changes in bestaande output-schema's of stappenstructuur.

- `documenten-audit`: 2.0.0 → **2.1.0** (punten 2, 4, 5, 7 raken skill-inhoud)
- `ecli-verificatie`: 2.0.0 → **2.1.0** (punten 1, 5, 6 raken skill-inhoud)
- `audit-synthese`: 1.0.0 → **1.1.0** (punt 1 raakt skill-inhoud)

Punt 3 (bulk-modus testdekking) wijzigt uitsluitend `tests/` — geen skill-inhoud, dus geen versiebump nodig.

## Niet in scope (bewust uitgesteld)

- **PII/persoonsgegevens-richtlijn** — relevant gezien het Woo/AVG-domein, maar de `ecli_lookup_V10.py`-toolkit's README bevestigt dat NL-bronnen al gepseudonimiseerd worden gepubliceerd door de Rechtspraak zelf; vermindert de urgentie voor NL-bronnen. EU/EHRM-bronnen zijn dat niet per se. Apart traject.
- **Round-trip-mechanisme** na Fase 3-correcties terug door Fase 1/2 — vermoedelijk bewust menselijk werk, niet vastgelegd.
- **Live ECLI-zoekhulp** via `rechtspraak_client.py`'s `zoek()`-functionaliteit (voor claims zonder ECLI waar de gebruiker naar ondersteunende jurisprudentie wil zoeken) — natuurlijke vervolgstap op punt 6, maar apart traject.

## Verificatie na implementatie

Zoals gebruikelijk in dit project:
```bash
python3 scripts/package_skills.py --validate-only
python3 scripts/generate_manifests.py --check   # na regenereren
python3 tests/test_pipeline_contracts.py
```
Plus: nieuwe testfuncties voor punt 3 (bulk-modus) moeten slagen, en de nieuwe `case-002`-fixture moet een volledige worked example zijn zoals `case-001` (input, expected output alle 3 fases, README).
