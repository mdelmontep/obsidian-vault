---
title: una guía de migración de modelo no es una lista de borrados — grep antes de aplicarla
date: 2026-08-01
source: claude-code-session
tags: [claude-code, prompting, opus5, harness]
---

La guía oficial de Opus 5 dice "quita las instrucciones de verificación de tus prompts: el modelo ya se auto-verifica y esto provoca sobre-verificación". Leído literal, invita a barrer los prompts propios. Aplicado a ciegas, habría borrado los gates deterministas.

**La distinción que la guía no hace explícita**, y que decide qué se toca:

- **Auto-verificación del modelo** = antipatrón real en Opus 5: "double-check tu respuesta", "añade un paso final de verificación", "usa un subagente para revisar tu trabajo". Compone mal con lo que el modelo ya hace solo y quema tokens.
- **Gate determinista y externo** = se queda intacto: `lint`/`typecheck`/`build`, `diff -rq`, `gh pr view`, smoke E2E, `git log origin/main..HEAD`. Un gate externo no es el modelo autoaprobándose — es justo lo que evita que lo sea. Coincide con "sin VERIFY no hay loop, hay agente autoaprobándose".

**Y grep antes de reescribir nada**: el barrido real sobre 180 skills propias, 9 commands, 18 agents y 14 `CLAUDE.md` de proyecto dio **0 hits**. Los 39 aparecieron solo en packs de terceros bajo `plugins/cache/` — que además **no se tocan**: se sobrescriben en la siguiente actualización del plugin. La guía describía un problema que no teníamos; el trabajo útil estaba en el otro lado, añadir lo que Opus 5 no trae de serie (concisión explícita, longitud de entregables en disco, scope cerrado, cap de subagentes).

Regla: ante guía de migración de modelo nuevo, primero medir con grep sobre lo propio, después decidir. Ver [[default-global-en-settings-anula-la-regla-condicional-del-claude-md]].
