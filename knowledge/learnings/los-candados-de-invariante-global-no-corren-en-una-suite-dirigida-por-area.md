---
title: los candados de invariante global no corren en una suite dirigida por área
date: 2026-08-15
source: claude-code-session
tags: [metodo, testing, agentes]
---

Un cron nuevo pasó su suite dirigida en verde y entró en `main` sin el `case` en
`admin/crons/run`: el botón «Run Now» habría devuelto *handler not wired*. Lo
cazó la suite COMPLETA, en un test que vive en `admin/`, no en `billing/`.

El patrón: los tests que protegen invariantes globales —«todo cron del registry
tiene handler», «toda ruta con sesión pasa por el wrapper», canarios que cuentan
kinds— **viven fuera del área que tocas por definición**, porque su trabajo es
mirar el conjunto. Una suite dirigida por el área del diff no los ejecuta jamás,
y en verde parece que todo está cubierto.

Muerde el doble con agentes en paralelo: cada uno corre su suite dirigida, todos
verdes, y `main` acaba rojo por candados que ninguno tocaba. Pasó dos veces en
el mismo día (14 ramas y luego una).

**Regla**: la suite dirigida vale mientras iteras; antes de PUSH va la completa,
una vez, en la rama ya rebasada. No es lento comparado con dejar `main` en rojo.

Relacionado: [[una-suite-en-verde-no-prueba-el-camino-real]] · [[un-candado-que-vive-en-tsc-es-invisible-para-la-suite-y-para-la-mutacion]]
