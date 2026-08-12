---
title: borrar la carpeta de un proyecto no borra su memoria de claude code, la deja huérfana
date: 2026-08-12
source: claude-code-session
tags: [claude-code, harness, memoria]
---
La memoria de sesión de Claude Code vive en `~/.claude/projects/<cwd-con-guiones-por-barras>/memory/`, indexada por la ruta exacta del `cwd`, no por el nombre del proyecto ni por ningún ID estable. Si la carpeta de trabajo se borra o se recrea en otra ruta, la memoria vieja no se pierde, pero queda huérfana bajo la ruta original — no se recupera sola.

Fix: para reutilizarla, copiar el contenido de `memory/` (revisando que no queden rutas absolutas obsoletas dentro) a la carpeta calculada para la NUEVA ruta — sustituir cada `/` del cwd por `-`. Ejemplo real: mover el proyecto de `/Users/x/simarro` a `/Users/x/Projects/simarro` requirió copiar `-Users-x-simarro/memory/` a `-Users-x-Projects-simarro/memory/` a mano.

Caso real: proyecto Simarro (automatización n8n/Retell/Kommo). La carpeta original vivía fuera del patrón `~/Projects/` y desapareció de disco sin dejar rastro (sin Papelera, sin Time Machine). La memoria de 6 sesiones (histórico may-jun) sobrevivió intacta en su ruta vieja; hubo que migrarla a mano al recrear el proyecto (12-ago-2026).
