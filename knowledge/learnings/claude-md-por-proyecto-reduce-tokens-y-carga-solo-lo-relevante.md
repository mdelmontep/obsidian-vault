---
title: claude-md por proyecto reduce tokens y carga solo lo relevante
date: 2026-04-21
source: claude-code-session
tags: [claude-code, optimizacion, tokens]
---

Claude Code carga `~/.claude/CLAUDE.md` en cada mensaje de cada conversación. Además, carga `<repo>/CLAUDE.md` solo cuando se arranca desde ese directorio.

Patrón para reducir consumo de tokens:
1. **Global** (`~/.claude/CLAUDE.md`): solo reglas de comunicación, workflow y entorno genérico (~150 líneas max)
2. **Por proyecto** (`<repo>/CLAUDE.md`): gotchas específicos del schema, frontend, deploy, etc. Solo se cargan al trabajar ahí
3. **Vault Stack/** (`Stack/n8n.md`, `Stack/retell/...`): conocimiento técnico profundo, cargado bajo demanda cuando se menciona el tema
4. **Memory files**: credenciales y referencias, consultados solo cuando hace falta

En nuestro caso, mover 49 gotchas mezclados del global a sus destinos correctos redujo el CLAUDE.md de 199 a 157 líneas (~21% menos tokens por mensaje).

La tabla de "lectura por tema" en el global actúa como índice — Claude lee el archivo Stack/ correspondiente solo cuando el usuario menciona ese tema, sin coste fijo.
