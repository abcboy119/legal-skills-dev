# Domeindocumentatie

Hoe de engineering-skills de domeindocumentatie van deze repo moeten gebruiken bij het verkennen van de codebase.

## Lees dit vóór je gaat verkennen

- **`CONTEXT.md`** in de repo-root, of
- **`CONTEXT-MAP.md`** in de repo-root als dat bestaat — dat wijst naar één `CONTEXT.md` per context. Lees elke context die relevant is voor het onderwerp.
- **`docs/adr/`** — lees de ADR's die het gebied raken waar je aan gaat werken. In multi-context-repo's ook `src/<context>/docs/adr/` voor context-specifieke beslissingen.

Bestaat een van deze bestanden niet, **ga dan stilzwijgend door**. Meld het ontbreken niet en stel niet voor ze vooraf aan te maken. De skill `/domain-modeling` (bereikbaar via `/grill-with-docs` en `/improve-codebase-architecture`) maakt ze lazy aan zodra termen of beslissingen daadwerkelijk worden vastgelegd.

## Bestandsstructuur

Single-context-repo (de meeste repo's — ook deze):

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Multi-context-repo (herkenbaar aan `CONTEXT-MAP.md` in de root):

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← systeembrede beslissingen
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specifieke beslissingen
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## Gebruik het vocabulaire van het glossarium

Zodra je output een domeinbegrip benoemt (in een issue-titel, een refactorvoorstel, een hypothese, een testnaam), gebruik dan de term zoals gedefinieerd in `CONTEXT.md`. Wijk niet uit naar synoniemen die het glossarium expliciet vermijdt.

Staat het begrip dat je nodig hebt nog niet in het glossarium, dan is dat een signaal — óf je verzint taal die het project niet gebruikt (heroverweeg), óf er is een echt gat (noteer het voor `/domain-modeling`).

## Meld ADR-conflicten

Spreekt je output een bestaande ADR tegen, benoem dat dan expliciet in plaats van hem stil te overrulen:

> _In strijd met ADR-0007 (event-sourced orders) — maar het is de moeite waard om te heropenen omdat…_
