---
title: contención de CPU entre sesiones paralelas puede parecer un bug de UI (skeleton/carga atascada)
date: 2026-07-15
source: claude-code-session
tags: [qa, cpu, multi-agente, worktree, debugging]
---

Con varias sesiones/worktrees Claude Code corriendo `next build`/`next dev` en
paralelo en la misma máquina (load average >10 en una máquina de 10 cores), una
vista que hace fetch real (200 OK verificado por red) puede quedarse VISUALMENTE
en skeleton/loading varios segundos — no por un bug de estado/acumulador, sino
porque el hilo principal de React/Fast Refresh está bloqueado compitiendo por CPU.
Diagnostiqué esto como "bug real" y delegué un fix antes de comprobar `uptime`;
un agente con la máquina descargada (load 4-8) no pudo reproducirlo ni una vez
tras esperas de 60s.

Antes de diagnosticar un "atasco" de UI como bug de código:
1. `uptime` + `ps aux | grep "next build"` — si hay contención real, es la primera
   sospechosa.
2. Esperar bastante más de lo intuitivo (30-60s, no 5s) antes de concluir "atascado".
3. Si hace falta delegar la investigación, pedir explícitamente reproducción con
   `uptime`/`ps aux` ANTES de tocar código, y que reporte "no reproducido" en vez de
   forzar un fix a código que no está roto.

**También invalida tandas de E2E enteras** (2026-07-27): con `next build` + vitest + Playwright a la
vez, 41 smokes murieron con `page.goto: Timeout 30000ms` y en aislado pasaban en segundos. Lo hice
DOS veces en la misma sesión. Corolario: mientras mides, no corres nada más; y si un test pasa solo
pero falla en la tanda larga, el sospechoso es la máquina. El gate real de una suite así es el
contenedor oficial, no el portátil.

**Y las Web Vitals**: el informe de CWV de la suite dio `CLS 0,31` en `/settings` y `0,20` en
`/dashboard` medidos en esa misma tanda cargada. En silencio son **0,045 y 0,023**: dos de los tres
"problemas de rendimiento" no existían. Cualquier métrica sensible al hilo principal (CLS, LCP, INP)
hay que medirla con la máquina libre o no vale.

**Y el gate local entero** (2026-07-30, AGH): con otro proyecto encima (`next build` + 2 `tsc` +
`vitest`, load **75** en 10 cores) `npm run gate` tardó **572 s** y dio 24 fallos —todos timeouts de
hooks `beforeEach` en tests `.pg` que en aislado pasan—. Con la máquina libre: **80 s y verde**. Regla:
si el gate tarda mucho más de lo habitual, mirar `sysctl -n vm.loadavg` ANTES que el diff; y un gate
corrido bajo saturación no se documenta en la PR **ni en verde ni en rojo**, porque no mide nada.
Síntoma de máquina ahogada de verdad: hasta `uptime` tarda >120 s.

Ver [[facturaia]] · [[agh-iberica]] · [[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]] · [[cero-mientras-carga-no-es-cero-vacio-y-provoca-cls]].
