---
title: edit no casa una línea "idéntica" → revisar bytes ocultos (byte nulo) con python repr
date: 2026-07-02
source: claude-code-session
tags: [claude-code, harness, gotcha, debugging]
---

Al escribir un template literal `` `${a} ${b}` `` con la tool Write, se coló un **byte nulo**
(`\x00`) en vez del espacio entre las interpolaciones. Síntoma: `Edit` fallaba con "String to
replace not found" sobre una línea que en el Read se ve idéntica, y `perl -0pi` tampoco casaba.

Fix / diagnóstico: cuando un `Edit` no casa una línea que parece exacta, no asumir "está bien" —
inspeccionar los bytes reales:
`python3 -c "print(repr(open('f').read().splitlines()[N]))"` → destapa `\x00`, CRLF, NBSP, etc.
Luego reemplazar con Python (`s.replace(old_con_\x00, new)`) y verificar que el fichero queda
libre de nulos. Raro, pero cuesta minutos si no se sospecha.

**Y el síntoma que NO es el de arriba (6-ago, AGH):** el mismo byte en un `.ts` **compila, pasa lint
y deja la suite en verde**. Lo que rompe es `grep`: `file` clasifica el fichero como `data` y grep
**suprime las coincidencias sin imprimir nada** (`-a` las devuelve). Si un grep deja de encontrar
algo que sabes que está, sospecha del FICHERO antes que del patrón. Pesa porque media docena de
candados barren por CONTENIDO (`grep -rl`): un fuente que grep no lee queda fuera de todos ellos y
el candado pasa a verde **por ausencia**. Ver [[un-guard-que-detecta-por-contenido-caza-los-comentarios-que-lo-niegan]].
