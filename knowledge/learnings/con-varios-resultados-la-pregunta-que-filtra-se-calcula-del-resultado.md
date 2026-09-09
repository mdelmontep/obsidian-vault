---
title: con varios resultados, la pregunta que filtra se calcula del resultado
date: 2026-09-09
source: simarro
tags: [voice, ux, n8n, retell]
---

Recitar dos de doce por teléfono no informa: el cliente no puede comparar y la conversación se atasca. Con 3 o más resultados, la respuesta útil es **una pregunta** — pero elegida por lo que de verdad separa lo que hay, no escrita caso a caso en el prompt.

Implementado en Simarro (9-sep-2026, nodo `Format For Voice`) como una cascada sobre el catálogo completo devuelto, no sobre las dos que se locutan:
1. ¿están repartidas por varios municipios? → pregunta por zona, nombrando los 3 más frecuentes.
2. ¿mismo municipio, tipos distintos? → "dos chalets y un piso, ¿qué prefieres?".
3. ¿mismo sitio y mismo tipo? → rango real de precios → "¿en qué presupuesto te mueves?".
4. Nada discrimina, o hay menos de 3 → recitar como siempre.

El orden hace además que no se repregunte lo que el cliente ya dijo: si pidió "chalet", el eje tipo colapsa solo y cae al siguiente. Cero zonas o tipos escritos a mano: si mañana entra cartera en otro municipio, la pregunta cambia sola.
