# Push deze repo naar GitHub/GitLab

Deze map is een complete git-repo met 5 commits en 4 tags. Hieronder staat hoe je hem naar een remote pusht.

## Wat zit erin

```
5 commits op main branch:
  ef3ddd6  v0: originele upload (pre-fixes)
  e677bd4  v1: Round 1 fixes (B1-B5 + K1 + K2)
  50a605a  v2: Round 2 fixes (K3-K6 + ecli_formaat_geldig)
  f49a02e  v3: Round 3 fixes (K7-K13 + P1-P8) — alle review-punten opgelost, 142/142 tests PASS
  f306d93  docs: push-instructies voor GitHub/GitLab (deze file)
```

Naast deze 5 commits op `main` zijn er 4 annotated tags die wijzen naar de eerste 4 commits:

```
v0-original      → ef3ddd6
v1-fixes-round1  → e677bd4
v2-fixes-round2  → 50a605a
v3-fixes-round3  → f49a02e
```

> De HEAD-commit (PUSH_INSTRUCTIONS.md) is niet getagd — dat is bewust, want deze commit bevat alleen documentatie over de repo zelf, geen pipeline-wijzigingen.

Gebruik `git log --oneline` en `git tag` om de lijsten zelf te bekijken.

## Stap 1 — Maak een lege remote aan

Op GitHub (of GitLab, Bitbucket, etc.) maak je een **lege** repository aan. Vink alle init-opties (README, .gitignore, license) uit — helemaal niets. Je hebt straks een URL nodig die er zo uitziet:

- SSH: `git@github.com:abcboy119/legal-skills.git`
- HTTPS: `https://github.com/abcboy119/legal-skills.git`

## Stap 2 — Voeg de remote toe

Pak deze repo-map lokaal uit (als hij als zip is geleverd), open een terminal erin, en voeg de remote toe:

```bash
cd legal-skills-git        # of hoe de map ook heet na het uitpakken

# Vervang door jouw eigen URL:
git remote add origin git@github.com:abcboy119/legal-skills.git
```

Controleer:

```bash
git remote -v
# origin  git@github.com:abcboy119/legal-skills.git (fetch)
# origin  git@github.com:abcboy119/legal-skills.git (push)
```

## Stap 2.5 — (Aanbevolen) Verifieer lokaal dat de repo klopt

Vóór je pusht, draai de drie checks die ook in CI draaien:

```bash
python3 scripts/package_skills.py --validate-only
python3 scripts/generate_manifests.py --check
python3 tests/test_pipeline_contracts.py
```

Als één van deze faalt, pas de bestanden dan eerst aan. Als alles groen is (3/3 skills valid, 3/3 manifests consistent, 142/142 tests PASS), ben je zeker dat je geen broken repo publiceert.

## Stap 3 — Push main én alle tags

```bash
git push -u origin main --tags
```

Dat commando duwt:
- De `main` branch met alle 5 commits.
- Alle 4 annotated tags (`v0-original`, `v1-fixes-round1`, `v2-fixes-round2`, `v3-fixes-round3`).

`-u` zet `origin/main` als upstream, zodat je daarna alleen `git push` hoeft te typen.

## Stap 4 — Verifieer op GitHub/GitLab

Open de repo in je browser. Je zou moeten zien:

- Op de hoofdpagina: alle v3-bestanden plus `PUSH_INSTRUCTIONS.md` (laatste commit op main).
- Onder "Commits": 5 commits met de beschrijvende berichten.
- Onder "Tags": 4 tags, klikbaar voor een release-pagina.

Optioneel: zet op GitHub onder "Releases" per tag een titel + release notes. Je kunt de corresponderende sectie uit `CHANGELOG.md` kopiëren als release description — dat geeft een mooie publieke changelog per versie.

## Stap 5 — (Optioneel) Author info corrigeren

De commits zijn nu gesigneerd met een tijdelijke lokale identity:

```
Author: Badr <badr@local>
```

Als je dat wilt veranderen vóór het pushen, kun je **alle** commits in één commando herschrijven met je echte identity:

```bash
# Zet je echte identity in de repo-config (niet --global als je per-repo wilt)
git config user.email "your@email.com"
git config user.name "Your Name"

# Herschrijf alle commits vanaf de root, met --reset-author per commit
git rebase --root --exec "git commit --amend --reset-author --no-edit"
```

Dit werkt in één keer voor alle 5 commits, zonder interactieve editor. **Let op:** de commit-hashes veranderen hierdoor. De 4 tags wijzen nog naar de oude hashes en worden niet automatisch meegenomen. Je moet ze opnieuw zetten:

```bash
# Vervang tags naar de nieuwe hashes (v0=HEAD~4, v1=HEAD~3, v2=HEAD~2, v3=HEAD~1)
git tag -f -a v0-original     HEAD~4 -m "Originele upload zoals ontvangen"
git tag -f -a v1-fixes-round1 HEAD~3 -m "Round 1: B1-B5 + K1 + K2"
git tag -f -a v2-fixes-round2 HEAD~2 -m "Round 2: K3-K6 + ecli_formaat_geldig"
git tag -f -a v3-fixes-round3 HEAD~1 -m "Round 3: K7-K13 + P1-P8 - alle review-punten opgelost"

# Verifieer
git log --oneline
git tag
```

Daarna gewoon `git push -u origin main --tags`.

> Alternatief voor geavanceerde gebruikers: `git filter-repo --mailmap mailmap.txt` of `git filter-branch`. Maar de rebase-methode hierboven is robuust genoeg voor 5 commits.

## Stap 6 — (Optioneel) Branch-protectie en CI

Zodra de repo op GitHub staat, kun je onder "Settings → Branches" de `main` branch beschermen (require pull request, require status checks). Voeg een GitHub Actions workflow toe in `.github/workflows/ci.yml`:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install jsonschema
      - run: python3 scripts/package_skills.py --validate-only
      - run: python3 scripts/generate_manifests.py --check
      - run: python3 tests/test_pipeline_contracts.py
```

Die CI draait bij elke push en PR dezelfde 3 checks die lokaal ook groen zijn.

## Veelvoorkomende problemen

**"fatal: remote origin already exists"**
Je had al een remote toegevoegd. Verwijder hem eerst: `git remote remove origin`, dan opnieuw toevoegen.

**"Updates were rejected because the remote contains work that you do not have"**
De remote is niet leeg — je hebt waarschijnlijk bij het aanmaken op GitHub toch een README of .gitignore aangevinkt. Maak op GitHub een **nieuwe, echt lege** repository aan, of verwijder de bestaande en maak opnieuw. Force-push (`git push -f`) kan ook, maar is overbodig riskant voor een verse repo — liever de remote netjes leeg maken.

**"Permission denied (publickey)"**
SSH-key niet ingesteld. Gebruik HTTPS-URL in plaats van SSH, of voeg je SSH-key toe aan GitHub via "Settings → SSH and GPG keys".

**Tags niet zichtbaar op GitHub**
Je vergat `--tags` in het push-commando. Achteraf alsnog: `git push origin --tags`.

**Na author-rewrite wijzen tags naar niet-bestaande commits**
Je hebt de rebase gedaan maar de tags niet ververst. Voer de `git tag -f -a ...` commando's uit Stap 5 uit, dan `git push -f origin --tags` om de tags op GitHub te overschrijven.

## Resultaat na push

Je hebt op GitHub een repo met:

- Een clean commit-geschiedenis die de hele evolutie van het project laat zien.
- 4 tags die als release-punten dienen.
- Per tag een release-pagina waarop je de changelog van die ronde kunt zetten.
- Een diff tussen twee tags direct in de UI te bekijken via `?compare=base...head`.

Zo kan een reviewer precies zien wat er in elke ronde is veranderd, en kan jij later altijd teruggrijpen op een eerdere versie.
