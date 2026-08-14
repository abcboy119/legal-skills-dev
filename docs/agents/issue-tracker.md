# Issue tracker: GitHub

Issues en specs voor deze repo leven als GitHub issues. Gebruik de `gh` CLI voor alle operaties.

## Conventies

- **Issue aanmaken**: `gh issue create --title "..." --body "..."`. Gebruik een heredoc voor meerregelige bodies.
- **Issue lezen**: `gh issue view <number> --comments`, comments filteren met `jq` en ook de labels ophalen.
- **Issues opsommen**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` met de juiste `--label`- en `--state`-filters.
- **Reageren op een issue**: `gh issue comment <number> --body "..."`
- **Labels toevoegen / verwijderen**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Sluiten**: `gh issue close <number> --comment "..."`

Leid de repo af uit `git remote -v` — `gh` doet dit automatisch binnen een clone.

## Pull requests als triage-oppervlak

**PRs als request-oppervlak: nee.** _(Zet op `ja` als deze repo externe PRs als feature requests behandelt; `/triage` leest deze vlag.)_

Op `ja` doorlopen PRs dezelfde labels en statussen als issues, met de `gh pr`-equivalenten:

- **PR lezen**: `gh pr view <number> --comments` en `gh pr diff <number>` voor de diff.
- **Externe PRs opsommen voor triage**: `gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments` en daarna alleen `authorAssociation` `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR` of `NONE` behouden (`OWNER`/`MEMBER`/`COLLABORATOR` laten vallen).
- **Reageren / labelen / sluiten**: `gh pr comment`, `gh pr edit --add-label`/`--remove-label`, `gh pr close`.

GitHub deelt één nummerruimte tussen issues en PRs, dus een kale `#42` kan beide zijn — los op met `gh pr view 42` en val terug op `gh issue view 42`.

## Als een skill zegt "publiceer naar de issue tracker"

Maak een GitHub issue aan.

## Als een skill zegt "haal het relevante ticket op"

Draai `gh issue view <number> --comments`.

## Wayfinding-operaties

Gebruikt door `/wayfinder`. De **map** is één issue met **child**-issues als tickets.

- **Map**: één issue met label `wayfinder:map`, met de body Notes / Decisions-so-far / Fog. `gh issue create --label wayfinder:map`.
- **Child-ticket**: een issue dat als GitHub sub-issue aan de map hangt (`gh api` op het sub-issues-endpoint). Waar sub-issues niet aanstaan: zet de child in een task list in de map-body en `Part of #<map>` bovenaan de child-body. Labels: `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Zodra geclaimd wordt het ticket toegewezen aan de uitvoerende dev.
- **Blokkering**: GitHub's **native issue dependencies** — de canonieke, in de UI zichtbare representatie. Voeg een edge toe met `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`, waarbij `<blocker-db-id>` het numerieke **database-id** van de blocker is (`gh api repos/<owner>/<repo>/issues/<n> --jq .id`, _niet_ het `#number` of `node_id`). GitHub rapporteert `issue_dependencies_summary.blocked_by` (alleen open blockers — de live gate). Waar dependencies niet beschikbaar zijn, val terug op een regel `Blocked by: #<n>, #<n>` bovenaan de child-body. Een ticket is gedeblokkeerd zodra elke blocker gesloten is.
- **Frontier-query**: som de open children van de map op (`gh issue list --state open`, beperkt tot de sub-issues / task list van de map), laat alles met een open blocker vallen (`issue_dependencies_summary.blocked_by > 0`, of een open issue in de `Blocked by`-regel) of met een assignee; de eerste in map-volgorde wint.
- **Claimen**: `gh issue edit <n> --add-assignee @me` — de eerste schrijfactie van de sessie.
- **Afronden**: `gh issue comment <n> --body "<antwoord>"`, dan `gh issue close <n>`, dan een context-pointer (gist + link) toevoegen aan Decisions-so-far in de map.
