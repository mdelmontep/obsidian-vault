---
title: autoDeploy sin watchPaths mata el trabajo en vuelo del worker, y sin handler de SIGTERM la culpa se la lleva otro
date: 2026-07-30
source: claude-code-session
tags: [dokploy, deploy, worker, observabilidad, facturaia]
---

Un servicio long-running (runner de tickets) con `autoDeploy` contra `main` y `watchPaths` VACÍO se
redespliega con **cada push del repo entero**: 10 deploys en un día, 8 de ellos de código que no era
suyo, y cada uno recreando el contenedor a mitad de una sesión de 20 min. El job moría siempre, y
como no había handler de señal quedaba en `ejecutando` sin latir: el watchdog lo cerraba 15 min
después con "runner sin latido", que apunta al agente y no al deploy. Diagnóstico por horas: el
último latido cae al segundo en el minuto del deploy (`compose.one` → `deployments[].createdAt`), y
`docker inspect` decía `OOMKilled: false`, `ExitCode: 0` — no había nada roto.

Hacen falta las dos mitades: (1) `watchPaths: ["ops/<servicio>/**"]`, o el worker se reinicia por
trabajo ajeno; (2) handler de SIGTERM que cierre lo que lleva en mano **con el motivo verdadero** y
`stop_grace_period` que dé tiempo al callback (los 10 s de Docker no siempre bastan).

Trampa del handler: al matar al hijo, el flujo normal sigue su curso y reporta su propio fallo
genérico ("salió con código null"), que llega ANTES y gana el compare-and-set — el estado vuelve a
mentir. Durante el apagado, el único que puede hablar del trabajo es el handler; lo demás se
silencia. Sale en un smoke con SIGTERM real, no leyendo el código.

Ver [[latido-que-solo-cubre-el-tramo-interesante-deja-el-resto-a-merced-del-watchdog]] · [[integracion-en-jsonb-tabla-generica-pierde-observabilidad]]
