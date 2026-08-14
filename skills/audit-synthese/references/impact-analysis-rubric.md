# Impact Analysis Rubric — Stap 1 (Gecorrigeerde impact)
> Bijbehorende stap in SKILL.md: Stap 1 (Impactanalyse per document).

## Classificatie van "Gecorrigeerde impact"

Loop de regels **in deze volgorde** af en gebruik de eerste die van toepassing is. De volgorde is dwingend: een document kan aan meerdere criteria voldoen (bijv. één tegengesproken kernclaim én overwegend ontbrekende bronnen), en dan weegt de zwaarste bevinding het zwaarst. Tel per document uitsluitend de claims die in de verificatie-JSON aan dat `doc_id` zijn gekoppeld.

1. **"Fundamenteel verzwakt wegens N tegengesproken kernclaim(s)"** — minstens één `TEGENGESPROKEN` claim die dragend is voor de kernconclusie van het document.
2. **"Verzwakt wegens N tegengesproken bijzaak-claim(s)"** — minstens één `TEGENGESPROKEN` claim, maar geen daarvan is dragend voor de kernconclusie.
3. **"Betrouwbaarheid onvaststelbaar wegens ontbrekende bronnen"** — meer dan 50% van de claims is `NIET_CONTROLEERBAAR`.
4. **"Deels bruikbaar na revisie"** — twee of meer claims zijn `GEDEELTELIJK` of `NIET_BEVESTIGD`.
5. **"Oordeel blijft overeind"** — alle overige gevallen: geen `TEGENGESPROKEN`, hooguit één `GEDEELTELIJK`/`NIET_BEVESTIGD`, en hooguit de helft `NIET_CONTROLEERBAAR`.

Formuleer de gekozen beschrijving analoog aan bovenstaande, aangevuld met de concrete aanleiding en de betrokken Claim_ID's — bijvoorbeeld *"Oordeel blijft overeind; C001 bevestigd, C002 onverifieerbaar wegens ontbrekende bron."*

Let op: regel 5 betekent **niet** dat alle claims bevestigd zijn. Een document met één bevestigde en één onverifieerbare claim valt hier ook onder; benoem die onverifieerbare claim dan expliciet in de toelichting, zodat de eindredacteur niet de indruk krijgt dat het document volledig is geverifieerd.
