---
title: el coste de una suite de evals es llamadas × prompt — mide el caché antes de proponerlo como ahorro
date: 2026-08-04
source: claude-code-session
tags: [evals, llm, coste, caching, metodo, agh]
---
Antes de proponer prompt caching como palanca de ahorro, **mídelo**. En AGH iba a proponerlo
y la sonda lo descartó: ya estaba al **98,5 %** y llevaba meses así sin que nadie lo supiera.

Sonda barata (3 llamadas idénticas al endpoint real, leyendo `usage`):
```
llamada 1: prompt_tokens=13.776  cached=4.992    (cache templándose)
llamada 2: prompt_tokens=13.776  cached=13.568   → 98,5 %
```
OpenAI: `usage.prompt_tokens_details.cached_tokens`. Anthropic: `cache_read_input_tokens`
(ver [[anthropic-prompt-cache-prefijo-system-tools]]).

Con eso sale el modelo de coste real, y suele desmontar el folclore: la corrida ×3 costaba
**~11,7 $**, no los 19 que decía la doc (ése era el precio *pre-caching*). La salida son 9-50
tokens y la entrada nueva el 1,5 % → **el coste es `nº de llamadas × tamaño del prompt`**.

Consecuencia de método: si el prompt no se puede encoger (encogerlo exige evals → circular),
**la única palanca es hacer menos llamadas**. No repetir N veces los casos deterministas:
de 217 casos fallaban 6, y repetíamos 211 dos veces de más. ⚠️ Si las repeticiones pasan a ser
adaptativas, la tasa debe calcularse como **media de tasas por caso** — si no, queda sesgada
hacia los que fallan y **re-baselinea todos los suelos en silencio**.
