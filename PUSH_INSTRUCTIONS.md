# Push deze repo naar GitHub/GitLab

Deze map is een complete git-repo met 4 commits en 4 tags. Hieronder staat hoe je hem naar een remote pusht.

## Wat zit erin

```
4 commits op main branch:
  v0-original     — originele upload (pre-fixes)
  v1-fixes-round1 — B1-B5 + K1 + K2
  v2-fixes-round2 — K3-K6 + ecli_formaat_geldig
  v3-fixes-round3 — K7-K13 + P1-P8 (alle review-punten opgelost, 142/142 tests PASS)
```

Elke tag is een annotated tag met een korte samenvatting. Gebruik `git log --oneline` en `git tag` om ze te zien.

## Stap 1 — Maak een lege remote aan

Op GitHub (of GitLab, Bitbucket, etc.) maak je een **lege** repository aan. Geen README, geen .gitignore, geen license — helemaal niets. Je hebt straks een URL nodig die er zo uitziet:

- SSH: `git@github.com:your-username/juridische-skills.git`
- HTTPS: `https://github.com/your-username/juridische-skills.git`

## Stap 2 — Voeg de remote toe

Pak deze repo-map lokaal uit (als hij als zip is geleverd), open een terminal erin, en voeg de remote toe:

```bash
cd juridische-skills-git        # of hoe de map ook heet na het uitpakken

# Vervang door jouw eigen URL:
git remote add origin git@github.com:your-username/juridische-skills.git
```

Controleer:

```bash
git remote -v
# origin  git@github.com:your-username/juridische-skills.git (fetch)
# origin  git@github.com:your-username/juridische-skills.git (push)
```

## Stap 3 — Push main én alle tags

```bash
git push -u origin main --tags
```

Dat commando duwt:
- De `main` branch met alle 4 commits.
- Alle 4 annotated tags (`v0-original`, `v1-fixes-round1`, `v2-fixes-round2`, `v3-fixes-round3`).

`-u` zet `origin/main` als upstream, zodat je daarna alleen `git push` hoeft te typen.

## Stap 4 — Verifieer op GitHub/GitLab

Open de repo in je browser. Je zou moeten zien:

- Op de hoofdpagina: de v3-bestanden (laatste commit).
- Onder "Commits": 4 commits met de beschrijvende berichten.
- Onder "Tags": 4 tags, klikbaar voor een release-pagina.

Optioneel: zet op GitHub onder "Releases" per tag een titel + release notes. Je kunt de commit-body kopiëren als release description.

## Stap 5 — (Optioneel) Author info corrigeren

De commits zijn nu gesigneerd met een tijdelijke lokale identity:

```
Author: Badr <badr@local>
```

Als je dat wilt veranderen vóór het pushen, kun je de geschiedenis herschrijven met `git rebase -i --root` en per commit de author aanpassen, of global config zetten vóór een amend-pass:

```bash
git config --global user.email "your@email.com"
git config --global user.name "Your Name"

# Herschrijf alle commits met deze identity:
git rebase -i --root
# In de editor: pik all commit lines en verander 'pick' in 'reword' (of laat staan en sla op)
# Daarna:
git commit --amend --reset-author --no-edit
git rebase --continue
# Herhaal voor elke commit
```

Of sneller met `git filter-branch` of `git filter-repo`, maar dat is geavanceerder.

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
De remote is niet leeg. Of je pusht naar de verkeerde repo, of iemand anders heeft al iets gepusht. Maak een nieuwe lege repo aan, of gebruik `git push -f origin main --tags` (force-push, overschrijft de remote — alleen doen als je zeker weet dat je de remote inhoud kwijt wilt).

**"Permission denied (publickey)"**
SSH-key niet ingesteld. Gebruik HTTPS-URL in plaats van SSH, of voeg je SSH-key toe aan GitHub via "Settings → SSH and GPG keys".

**Tags niet zichtbaar op GitHub**
Je vergat `--tags` in het push-commando. Achteraf alsnog: `git push origin --tags`.

## Resultaat na push

Je hebt op GitHub een repo met:

- Een clean commit-geschiedenis die de hele evolutie van het project laat zien.
- 4 tags die als release-punten dienen.
- Per tag een release-pagina waarop je de changelog van die ronde kunt zetten.
- Een diff tussen twee tags direct in de UI te bekijken via `?compare=base...head`.

Zo kan een reviewer precies zien wat er in elke ronde is veranderd, en kan jij later altijd teruggrijpen op een eerdere versie.
