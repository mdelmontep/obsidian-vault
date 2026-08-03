---
title: los tests rojos que hereda un merge se clasifican uno a uno, no se actualizan en bloque
date: 2026-08-03
source: claude-code-session
tags: [tests, merge, gates]
---
Al mergear `main` en una rama vieja llegan tests que la rama nunca vio. Todos rojos a la vez
invitan a la misma acción —actualizar los valores esperados— y ahí se cuela el que sí estaba
midiendo una regresión real.

Cada rojo cae en uno de dos cubos, y hay que decidirlo por separado:
- **Asserta un dato que cambió legítimamente** (copy, cifra, texto de un heading) → actualizar
  el esperado. El contrato que fija el test no se toca.
- **Asserta una regla del repo** (a11y, físicalidad del motion, capas, seguridad) → arreglar el
  código, nunca el test. Este es el que el merge estaba ahí para cazar.

Caso real (agentesia-web, 03-ago): 5 rojos tras el merge. Cuatro eran copy del titular
anterior; el quinto era un lint de motion que prohíbe entradas por debajo de `scale: 0.9` y
pillaba dos `0.5`/`0.6` de una ilustración nueva. Actualizar los cinco habría dejado pasar el
único que importaba. Ver [[el-gate-verde-no-sustituye-una-revision-adversarial-antes-de-mergear]]
