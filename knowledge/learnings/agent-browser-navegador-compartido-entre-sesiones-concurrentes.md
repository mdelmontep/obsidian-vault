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

**Y contamina también los smokes contra PROD** (30-jul): a mitad de un smoke en
`app.tufacturaia.com` el navegador apareció en `localhost:3002`, el dev server de
otra sesión. Se detectó porque el snapshot traía "Open Next.js Dev Tools", que en
prod no existe. Corolario: en un smoke de producción, `agent-browser eval
"location.href"` **en cada paso que escriba algo** — un `open` que devuelve la URL
correcta no garantiza que el siguiente comando siga en esa pestaña.

**El síntoma que lo delata sin salir de una sola sesión** (14-ago): la sesión `default` arrastraba
una pestaña vieja de otra corrida y **`snapshot` contestaba de una página distinta que `eval`/`get
url`** — dos comandos seguidos describiendo pantallas diferentes. Si eso pasa, no es el sitio: es el
perfil compartido. `--session <nombre>` propio y a empezar de cero.

