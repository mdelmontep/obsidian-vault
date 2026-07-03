---
title: agent-browser sin --session comparte navegador/cookies con otras sesiones Claude Code concurrentes en localhost
date: 2026-07-04
source: claude-code-session
tags: [agent-browser, testing, worktree, multi-agent]
---

Con varios worktrees/sesiones Claude Code activos en el mismo Mac, cada uno con su
propio `npm run dev` en un puerto distinto: `agent-browser open http://localhost:PUERTO`
sin `--session <nombre>` reusa el **mismo daemon/perfil de Chrome por defecto** de
todas las sesiones. Síntomas reales:
- Al abrir `/login` en el puerto propio, apareció ya logueado — cookie de sesión
  de OTRA sesión (`localhost` sin scope de puerto en el navegador).
- Navegación aparentemente aleatoria a `about:blank` o a la URL de OTRO puerto tras
  un click — otra sesión ejecutó un comando `agent-browser` sobre la misma pestaña
  en paralelo, pisando el estado.

Fix: **siempre** `agent-browser --session <nombre-unico-de-tarea> <comando>` (o
`export AGENT_BROWSER_SESSION=<nombre>`) desde el primer comando, incluso para
smoke tests de un solo uso. Cada `--session` es un perfil de Chrome aislado
(cookies/tabs/refs propios) — sin esto, cualquier smoke con más de una sesión
Claude Code activa en la máquina es sospechoso de contaminación cruzada.
