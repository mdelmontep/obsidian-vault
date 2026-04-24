---
title: remote triggers de claude probablemente bloquean curl en sandbox
date: 2026-04-25
source: claude-code-session
tags: [claude-code, triggers, sandbox]
---

Los Remote Triggers (scheduled) de Claude Code ejecutan correctamente (`run` devuelve HTTP 200) y pueden leer repos de GitHub, pero las llamadas de red salientes (curl a Slack, fetch a APIs externas) probablemente están bloqueadas en el sandbox.

Evidencia: el mismo curl que funciona perfecto desde Claude Code local no produce resultado cuando se ejecuta desde el trigger remoto. El token de Slack es válido (verificado), el user ID es correcto (verificado), pero el mensaje nunca llega.

Workaround pendiente: que el trigger genere el resultado y lo persista en un archivo del repo, y un sistema externo (n8n webhook, GitHub Action) lo recoja y lo envíe al destino.
