---
title: si la config define una escalera ordenada, el invariante es el orden, no el min/max de cada campo
date: 2026-07-25
source: claude-code-session facturaia
tags: [validacion, backend, config, cobros]
---

Validar `min`/`max` por campo no protege una config cuyos campos forman una **secuencia**. Cada valor
puede ser legal por separado y el conjunto estar al revés.

Caso real TuFacturaIA (agente de cobros): la cadencia son tres campos (1er aviso D+3, 2º D+10, último
D+25). El orden `d1 < d2 < d3` **solo se validaba en el cliente**; el servidor comprobaba rangos por
campo. Y el consumidor elige nivel con una cascada `>= d3` primero. Con 90/3/7 guardado por API o
desde el panel de admin, una factura a 10 días entra directa como **nivel 3**, cuyo texto es "última
comunicación antes de iniciar procedimientos de reclamación formales". Sería el primer mensaje que
recibe un cliente final.

Reglas:
1. Validación cross-field **en servidor**, sobre el objeto **mergeado** (`{...defaults, ...guardado,
   ...patch}`). Sin el merge, un PATCH parcial de un solo campo pasa por vacío.
2. Misma regla en todas las puertas: web, API pública y panel de admin.
3. Si hay CHECK en BD, mapear su `23514` a 422 con mensaje por campo, no dejarlo salir como 500.
4. Validar la escritura **no repara el pasado**: inventariar las filas ya desordenadas antes de dar
   el fix por cerrado, y comprobar si ya llegaron mensajes con el tono equivocado.

Corolario general: una cascada `if (x >= mayor) … else if (x >= medio) …` transforma "config
desordenada" en "se elige la rama más agresiva", que es el peor fallo posible por defecto.
