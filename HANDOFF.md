# Handoff: legal-skills-dev — ontwerpronde ophaalbrug + compleet Claim Register

**Datum:** 2026-08-14
**Voor:** een verse agent die de vervolgsessie opent (sessie bewust gepauzeerd: "we gaan later verder")
**Status op moment van overdracht:** plan ter review; reviewronde 1 is verwerkt (drie gaten gedicht in het design-doc); repo is gecommit én gepusht; implementatie is nog NIET gestart.

## Waar we staan

Deze conversatie voerde de opdracht uit `docs/handoff/2026-08-14-research-dan-grilling.md`:

1. **Stap 1 (/research)** — afgerond. Primaire-bronnenonderzoek naar volledige uitspraaktekst per ECLI-kanaal (NL/EU/EHRM).
2. **Stap 2 (/grill-with-docs)** — afgerond. 14 vragen gesteld en beantwoord; de gebruiker koos overal zelf de optie, inclusief **Q14=(a)** (rubric-regels 3/4 tellen uitsluitend dragende beweringen).
3. **Plan opgeslagen** (`docs/superpowers/specs/2026-08-14-ophaalbrug-en-compleet-register-design.md`) en **reviewronde 1 verwerkt**: alle feitelijke claims van de review zijn tegen de repo geverifieerd; drie reële gaten zijn in het design-doc gedicht:
   - **Gat 1 (README.md):** punt 18 toegevoegd — versietabel → 2.2.0 / 2.2.0 / 1.3.0 (sync-checklist eist dit; geen CI-dekking).
   - **Gat 2 (Q8-strikte lezing):** test 37 krijgt een uitkomst-afhankelijke assertie op de "secundaire bron"-clausule, zodat een latere agent die niet per ongeluk terugzet/forceert zonder dat CI breekt.
   - **Gat 3 (C004):** `case-001/README.md` krijgt een expliciete regel dat `Dragend=Ja` voor C004 bewust is behouden (least-surprise, niet herclassificatie).
   - **Punt 19 (optioneel, nog ter beslissing gebruiker):** README-versie-contracttest die de README-versietabel koppelt aan de `version:`-frontmatter van de drie SKILL.md's.
4. **Laatste gebruikersinstructie:** "ja alles bijwerken en handoff ook bijwerken, commit en push daarna" — alles bijgewerkt, **gecommit én gepusht**:
   - `0d512b8` chore: versiebump naar 2.1.1/2.1.1/1.2.0 voor consistentieronde
   - `c41ba40` docs: repo-docs (CLAUDE.md, CONTEXT.md, agents) en research + ontwerp ophaalbrug-register-ronde
   - Beide op `origin/main`; working tree schoon. Vóór de commits is de volledige CI-drievoud gedraaid: 3/3 skills valid, 3/3 manifests consistent, 196 PASS / 0 FAIL.

Er is nog **geen** implementatie van het design-doc gestart; niets aan skills/tests/fixtures is in deze ronde gewijzigd (de skills-commits zijn de vorige v2.1.1/1.2.0-ronde).

## Artefacten (lezen, niet herhalen)

| Pad | Inhoud |
|---|---|
| `docs/handoff/2026-08-14-research-dan-grilling.md` | De oorspronkelijke opdracht (Stap 1 + 2, agenda, bevindingen) |
| `docs/research/2026-08-14-ecli-volledige-uitspraaktekst-nl-eu-ehrm.md` | Stap 1-resultaat: kanalen, dekkingscijfers, de stille-leeg-valkuil, 9 open vragen |
| `docs/superpowers/specs/2026-08-14-ophaalbrug-en-compleet-register-design.md` | **Het volledige plan** — besluiten Q1–Q14, versiebumps (2.2.0/2.2.0/1.3.0), wijzigingen per skill, fixtures (C003, C006, Dragend), testwijzigingen + nieuwe test 37 (incl. uitkomst-afhankelijke Q8-assertie), ADR-concepten 0001/0002, exacte CONTEXT.md-teksten, uitvoeringsvolgorde, validatiecommando's, review-verwerking en de resterende vlaggen |
| `CLAUDE.md` | Repo-regels die de implementatie bepalen: contracttests koppelen aan letterlijke strings, `references/MANIFEST.json`-hashes regenereren, `output.schema.json` bestaat byte-identiek tweemaal, handgeschreven frontmatter-parser, ECLI-conventie `"N/A"`, verplichte versiebump + `last_updated` |
| `docs/conventions.md` §7 + `docs/sync-checklist.md` | Volledige wijzigingsprocedure per skill |

## Volgende stappen voor de verse agent

1. **Lees eerst** `CLAUDE.md` en het design-doc (status: "voorgesteld — ter review"; reviewronde 1 verwerkt).
2. **Vraag de gebruiker om expliciete go/no-go** op de resterende punten (staan als "Open punten / vlaggen" in het design-doc):
   - het plan als geheel,
   - vlag 1: Q8-strikte lezing — óók de `LAAG`-clausule "secundaire bron" verwijderen? (de uitkomst wordt hoe dan ook gepind in test 37),
   - vlag 2: C004 op `Dragend = Ja` houden — in het plan vastgelegd als expliciete keuze in de case-001 README; herlabelen is een aparte bewuste keuze,
   - punt 19 (optioneel): README-versie-contracttest toevoegen of niet.
   - (Vlag 3/commit-strategie is opgelost: zie commits `0d512b8` + `c41ba40` op `origin/main`.)
3. **Implementeer na akkoord** in de volgorde uit het design-doc (CONTEXT/ADR's/docs → Fase 1 → Fase 2 → Fase 3 → fixtures → tests → MANIFEST → CHANGELOG → README). Eén fase tegelijk, valideren na elke fase.
4. **Validatiegate:** de drie commando's uit het design-doc (`package_skills.py --validate-only`, volledige testsuite — verwachting 37 testfuncties groen, `generate_manifests.py --check`). Bij een failure: eerst rapporteren vóór fixen — de tests zijn tekstgekoppeld, herformuleren van een zin breekt bewust een test (zie CLAUDE.md).
5. **Commit niet** zonder expliciete gebruikersopdracht.

## Suggested skills voor de verse agent

- **superpowers:executing-plans** — het goedgekeurde design-doc is het plan; voer het uit met review-checkpoints.
- **superpowers:verification-before-completion** — geen groen-CI-bewering zonder de drie validatiecommando's daadwerkelijk gedraaid te hebben.
- **git-workflow-and-versioning** — versiebumps en CHANGELOG-sectie; repo is net gecommit/gepusht (baseline `c41ba40`), committen alleen na gebruikersopdracht.
- **documentation-and-adrs** — ADR 0001 en 0002 volgens de concepten in het design-doc.
- **superpowers:systematic-debugging** — als een contracttest breekt; oorzaak zoeken in de tekstkoppeling, niet blind strings aanpassen.
- **superpowers:receiving-code-review** — als er nog een reviewronde komt: eerst verifiëren tegen de repo, dan pas implementeren.
- **ContextScout** (subagent) — voor context-ontdekking conform de project-workflow, vóór implementatie.
- **Niet opnieuw:** brainstorming/grilling — alle besluiten staan vast in het design-doc.

## Redactie

Geen gevoelige informatie (API-keys, wachtwoorden, PII) aangetroffen in deze conversatie; niets te redacteren. De commits bevatten uitsluitend skill-docs, tests en documentatie — geen secrets (voor het committen gescand).
