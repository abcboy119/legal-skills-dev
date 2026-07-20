# ECLI-Scanner Cross-check — optionele stap vóór Stap 9
> Bijbehorende stap in SKILL.md: Stap 9 (Claim Register).

Fase 1's ECLI-extractie in Stap 9 gebeurt volledig door het LLM, zonder ingebouwde cross-check. Twee risico's blijven daardoor ongedekt: het LLM **mist** een ECLI die wél in de brontekst staat, of het LLM **verzint** een ECLI die niet voorkomt. Deze optionele stap dekt beide af met een deterministisch (niet-LLM) hulpmiddel.

## Wanneer te gebruiken

**Optioneel.** Alleen relevant als de gebruiker een los scanner-script (bijv. `ecli_scanner.py`, niet onderdeel van deze repo) heeft gedraaid over dezelfde brondocumenten vóór of tijdens de audit, en de output daarvan aanlevert. Zonder die output verandert er niets aan de normale Stap 9-procedure.

## Procedure

1. De gebruiker levert de scanner-output aan (een lijst van ECLI's die deterministisch in de brondocumenten zijn gevonden, eventueel met validatiestatus).
2. Vergelijk deze lijst met de ECLI's die in Stap 9 zijn geëxtraheerd.
3. **ECLI door het LLM geëxtraheerd, niet in de scanner-lijst** → extra kritisch: zet `Extractie_Zekerheid = LAAG` en voeg in de kolom Opmerking toe: "Niet bevestigd door deterministische scan — mogelijke hallucinatie, extra controle aanbevolen."
4. **ECLI in de scanner-lijst, niet als claim opgenomen** → niet automatisch toevoegen (niet elke vermelding is een dragende claim), maar signaleer dit in Stap 8 (Lacunes en vervolgstappen) als een te controleren punt.
5. Rapporteer in Stap 1 kort of een scanner-cross-check is uitgevoerd en wat de uitkomst was.

## Wat dit niet is

Dit is geen vervanging van de ECLI-formaatcontrole (regex) uit Stap 9 — die blijft verplicht. Dit is een aanvullende, optionele cross-check op *volledigheid en juistheid van extractie*, niet op *syntax*.
