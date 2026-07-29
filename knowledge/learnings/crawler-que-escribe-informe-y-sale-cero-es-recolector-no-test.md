---
title: un crawler que escribe informe y sale 0 es un recolector, no un test
date: 2026-07-30
source: claude-code-session
tags: [testing, e2e, playwright, ci, verificacion]
---
El explorer E2E de TuFacturaIA recorría la app, apuntaba cada `pageerror` en `report.json`
y **pasaba con que hubiera visitado una página**. O sea: podía coleccionar la aplicación
entera rota y terminar en verde. Por eso Remesas SEPA estuvo caída en producción sin que
saltara nada, teniendo un test que la visitaba.

Vive en `tests/`, se llama `.spec.ts`, sale 0 → todo el mundo lo lee como cobertura. Un
recolector disfrazado de test es peor que no tenerlo, porque ocupa su hueco.

Dos preguntas al revisar cualquier checker (crawl, audit, lint script, verificador de loop):
1. ¿Qué hallazgo concreto lo pone en rojo? Si no hay ninguno, no es un checker.
2. ¿Está enganchado a CI? El nuestro falla desde el PR #1365, pero solo corre `visual.yml`
   en Actions, así que hoy sigue sin enterarse nadie. Fallar y no ejecutarse son lo mismo.

Mismo criterio que "sin VERIFY no hay loop, hay agente autoaprobándose" (CLAUDE.md).
