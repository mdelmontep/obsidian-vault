---
title: agent-browser auth login sin --session no deja sesión usable para el comando siguiente
date: 2026-07-29
source: claude-code-session
tags: [agent-browser, autenticacion, verificacion]
---

`agent-browser auth login fia` responde `✓ Logged in as 'fia'` y **cierra su navegador**. El
comando siguiente lanza uno nuevo, sin cookies, y cae en `/login?redirect=…`. Se lee como
"caducó la sesión" y manda a buscar credenciales que no hacen falta.

Secuencia que sí funciona: **abrir la sesión nombrada primero y pasar `--session` en TODO**.

```
agent-browser close --all
agent-browser open --session s1
agent-browser auth login fia --session s1
agent-browser get url --session s1      # → /dashboard
```

Otros detalles del CLI que muerden el mismo día: `screenshot` toma la ruta **posicional**
(`screenshot ruta.png`, no `--path`); `find <locator> <valor> <acción>` solo acepta
`click|fill|check|hover|text` (no `first`); no existe `resize`.

Ver [[agent-browser-eval-contexto-persiste-const-usar-iife]] · [[agent-browser-navegador-compartido-entre-sesiones-concurrentes]]
