# Push deze repo naar GitHub/GitLab

Deze map is een complete git-repo. Hieronder staat hoe je hem naar een remote pusht.

## Wat zit erin

De commit- en tag-geschiedenis groeit met elke ronde fixes, dus deze file houdt geen vaste aantallen of hashes bij (die raken meteen verouderd). Bekijk de actuele staat zelf voordat je pusht:

```bash
git log --oneline   # volledige commit-geschiedenis
git tag             # bestaande tags (kan leeg zijn — dat is normaal, tags zijn optioneel)
```

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

Als één van deze faalt, pas de bestanden dan eerst aan. Als alles groen is (3/3 skills valid, 3/3 manifests consistent, alle tests PASS), ben je zeker dat je geen broken repo publiceert.

## Stap 3 — Push main én eventuele tags

```bash
git push -u origin main --tags
```

Dat commando duwt de `main` branch plus alle lokale tags (als je die hebt aangemaakt — zie Stap 5). `-u` zet `origin/main` als upstream, zodat je daarna alleen `git push` hoeft te typen.

## Stap 4 — Verifieer op GitHub/GitLab

Open de repo in je browser. Je zou moeten zien:

- Op de hoofdpagina: de laatste stand van de bestanden plus de meest recente commit.
- Onder "Commits": dezelfde geschiedenis als lokale `git log --oneline`.
- Onder "Tags": alleen zichtbaar als je zelf tags hebt aangemaakt en gepusht.

Optioneel: zet op GitHub onder "Releases" per tag (indien aanwezig) een titel + release notes. Je kunt de corresponderende sectie uit `CHANGELOG.md` kopiëren als release description — dat geeft een mooie publieke changelog per versie.

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

Dit herschrijft **alle** commits vanaf de root, zonder interactieve editor. **Let op:** de commit-hashes veranderen hierdoor. Als je al tags had gezet (`git tag`), wijzen die nog naar de oude hashes en worden niet automatisch meegenomen — je moet ze opnieuw zetten met `git tag -f -a <naam> <nieuwe-hash> -m "<boodschap>"` voor elke bestaande tag. Verifieer met:

```bash
git log --oneline
git tag
```

Daarna gewoon `git push -u origin main --tags` (voeg `-f` toe voor tags als je bestaande tags op de remote overschrijft).

> Alternatief voor geavanceerde gebruikers: `git filter-repo --mailmap mailmap.txt` of `git filter-branch`.

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
      - run: pip install -r requirements.txt
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
- (Optioneel, als je tags hebt gezet) tags die als release-punten dienen, elk met een eigen release-pagina voor changelog-notities.
- Een diff tussen twee commits/tags direct in de UI te bekijken via `?compare=base...head`.

Zo kan een reviewer precies zien wat er in elke ronde is veranderd, en kan jij later altijd teruggrijpen op een eerdere versie.
