# Context Budget — Fase 1 strategie voor veel of lange brondocumenten
> Bijbehorende regel in SKILL.md: `<rules>`.

Dit lost een ander probleem op dan `ecli-verificatie/references/context-budget.md`. Fase 2's probleem is "één lange uitspraak tegen veel claims verifiëren"; Fase 1's probleem is "veel of lange brondocumenten auditen en onderling vergelijken". Beide gebruiken batching, maar de eenheid en de volgorde verschillen.

## 1. Basisprincipe: batchgewijs documenten verwerken

Bij meer dan ~8 documenten, of bij documenten die individueel een aanzienlijk deel van het contextvenster innemen, verwerk je niet alle documenten in één keer. Verdeel ze in batches van ongeveer 5 documenten (kleiner bij zeer lange individuele documenten, groter bij korte).

Procedure per batch:
1. Voer Stap 1 t/m 9 uit voor de documenten in deze batch, alsof het een audit op zichzelf is.
2. Ken `Doc_ID`'s en `Claim_ID`'s toe die doorlopen vanaf waar de vorige batch is geëindigd (zie §2).
3. Bewaar een korte lopende samenvatting (2-3 zinnen per document) om in latere batches terug te kunnen verwijzen zonder de volledige eerdere documenten opnieuw in context te laden.

## 2. Consolidatie: doorlopende nummering, geen botsingen

- `Doc_ID`'s lopen door over batches heen: batch 1 gebruikt Document 1-5, batch 2 gebruikt Document 6-10, enzovoort. Nooit hernummeren binnen een audit.
- `Claim_ID`'s lopen eveneens door: als batch 1 eindigt op C012, begint batch 2 bij C013.
- Na de laatste batch worden Stap 2 (thematische analyse), Stap 3 (vergelijkende analyse), Stap 5 (standpuntenvergelijking) en Stap 7 (best onderbouwde antwoord) uitgevoerd op basis van de lopende samenvattingen van álle batches samen, niet opnieuw op de volledige brondocumenten.
- Het uiteindelijke Claim Register (Stap 9) en Manifest (Stap 10) zijn de samenvoeging van alle batches — geen dubbele `Claim_ID`'s, geen gaten.

## 3. Volgorde van verwerken

Geen vaste inhoudelijke prioriteit zoals bij Fase 2 (die claims op zekerheid rangschikt) — hier is de volgorde gewoon de aanlevervolgorde van de documenten, tenzij de gebruiker een andere volgorde aangeeft. Verwerk batches sequentieel, niet gelijktijdig (elke batch bouwt voort op de lopende samenvatting van de vorige).

## 4. Signalen dat het budget wordt overschreden

- Een batch van 5 documenten past nog steeds niet ruim in het contextvenster (bijv. omdat één document zelf al zeer lang is).
- Je merkt dat je bij het schrijven van Stap 9 al vergeten bent wat er in een document uit een eerdere batch precies stond, ondanks de lopende samenvatting.

In die gevallen: verklein de batchgrootte (bijv. naar 2-3 documenten), en vermeld in Stap 1 expliciet dat batching is toegepast en met welke batchgrootte.

## 5. Rapportage in Stap 1

Vermeld kort of batching is toegepast: aantal documenten, aantal batches, batchgrootte. Voorbeeld: *"12 documenten aangeleverd; verwerkt in 3 batches van 4 documenten, doorlopend genummerd Document 1-12."*
