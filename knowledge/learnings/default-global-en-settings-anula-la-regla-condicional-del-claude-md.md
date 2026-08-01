---
title: un default global en settings.json anula la regla condicional escrita en CLAUDE.md
date: 2026-08-01
source: claude-code-session
tags: [claude-code, harness, settings, opus5]
---

`~/.claude/CLAUDE.md` decía "razonamiento alto cuando: arquitectura con trade-offs, debug sin hipótesis, seguridad, decisiones irreversibles". `~/.claude/settings.json:182` tenía `"effortLevel": "medium"` fijo, heredado de Opus 4.8. La regla **no podía cumplirse nunca**: el techo lo pone la config, no el prompt. Y no da error — simplemente las tareas duras corrían por debajo de lo que la regla pedía, en silencio, durante semanas.

Familia conocida: los modelos leen, los hooks bloquean. Aquí, **el settings manda y el CLAUDE.md solo aspira**. Una instrucción en prompt que pide subir algo que la config fija por debajo es decorativa.

Patrón general: cuando una regla del prompt hable de una palanca que también existe como setting (effort, modelo, permisos, timeouts), verificar el setting antes de dar la regla por viva. Si el setting es un techo, la regla del prompt solo puede bajar, nunca subir.

Fix aplicado: `effortLevel` a `high` (el default oficial de Opus 5) y bajar puntualmente en tareas mecánicas, en vez de un `medium` fijo que impedía subir. Barrido de validación pendiente en `top-of-mind`. Ver [[guia-de-migracion-de-modelo-no-es-lista-de-borrados-grep-antes]].
