---
title: n8n switch con conditions sin bloque options enruta todo por la primera salida
date: 2026-07-28
source: claude-code-session
tags: [n8n, switch, clinica-zen]
---
Un nodo Switch cuyas `rules.values[].conditions` no llevan el bloque
`options: {caseSensitive, typeValidation, version: 2}` ni `combinator` se evalúa con
semántica laxa: la PRIMERA regla se traga todos los items y las demás salidas reciben 0.
No da error — el workflow termina en verde por la rama equivocada.

Caso real (Clínica Zen, `PJBMjLLE0vNJjZH8`): item con `tipoRecordatorio: "4h"` salió por
la rama 0 (la de `"24h"`); la rama 1 quedó a 0 items. Todos los avisos de 4 horas llevaban
meses enviándose con la plantilla de 24 horas (`bot_id` 63810 en vez de 63808).

Se detecta SOLO en el `runData` de una ejecución: `data.main` por rama con el conteo de
items, no en el editor. Al construir un Switch por API, copiar el bloque `options` completo
de un IF sano del mismo workflow. Ver [[clinica-zen]]
