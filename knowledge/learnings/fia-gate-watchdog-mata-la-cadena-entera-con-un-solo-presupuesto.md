---
title: el watchdog de fia-gate mataba la cadena entera con un solo presupuesto
date: 2026-07-29
source: claude-code-session
tags: [claude-code, harness, fia-gate, macos]
---

`is_simple_chain` solo trocea cadenas con `&&` y **rechaza** las que llevan `;`, `|` o comillas —
o sea, casi cualquier comando real (`npm run lint 2>&1 | tail`). Un `lint; typecheck; vitest`
llegaba entero a `run_seg` con **un único TIMEOUT (900 s)**, y con la máquina cargada el lint solo
ya se lo comía: el watchdog lo mataba a mitad y devolvía `rc=143` sin decir nada. Se diagnostica
como OOM o como el harness.

**Antes de teorizar, mirar `~/.claude/gate/state/events.jsonl`**: un evento `timeout` con
`running→timeout = 900s` exactos lo cierra en un minuto. Yo lo achaqué a `reap_orphans` (heurística
"PPID 1 = huérfano") y era falso; lo que pareció confirmarlo —invocar
`node ./node_modules/typescript/bin/tsc` sí terminaba— era que esa ruta **no casa el patrón del
hook y corría SIN gate**, saltándose el semáforo. Un workaround que funciona porque desactiva la
protección no es un fix.

Arreglado 2026-07-29: el presupuesto se escala al nº de comandos pesados del segmento
(`count_heavy`) y el watchdog avisa por stderr al matar. Ver [[fia-gate]].

**El kill se disfraza de error ajeno.** El `pre-commit` de facturaia lee el exit no-cero como fallo
de tipos y aborta con "errores de TypeScript"; el mensaje real estaba dos líneas antes:
`.githooks/pre-commit: line 84: NNNNN Terminated: 15`. Bajo carga alta ese cartel miente — buscar
`Terminated` antes de creérselo. En un caso tapó además un error de tipos REAL.

**Sigue vivo para el gate COMPLETO (31-jul).** `npm run gate` (lint+typecheck+test+build) supera
los 900 s por sí solo, así que muere con `status: killed` y sin explicación. Correrlo **por
segmentos separados** —una llamada por etapa— es la forma de pasarlo, no un apaño. Y dos trampas
de medición del mismo día, las dos productoras de falsos verdes:
- `npm run gate | tail -30` devuelve **el exit code de `tail`**, o sea 0 siempre: di por bueno un
  gate que había fallado 1 fichero. Redirigir a un log y leer `$?`, nunca canalizar a `tail`.
- Con 3 gates a la vez (setup 404 s, tests a 5 s) caen tests por contención. **Un gate cada vez**;
  antes de diagnosticar un rojo, repetirlo en solitario.

**Reincidencia 19-ago**: cadena `lint; typecheck; build; vitest` con `;` → un solo presupuesto de
900 s → `killed` a los 15m01s clavados, dos veces. Volví a achacarlo a `reap_orphans` sin abrir
`events.jsonl` (el mismo diagnóstico falso de arriba) y monté un plan con tmux que no hacía falta.
El fix `count_heavy` del 29-jul solo cubre cadenas con `&&`: las de `;` siguen entrando enteras.
Regla que sí funcionó: **una etapa por llamada** (typecheck solo, luego build+vitest).

**No lanzar N agentes que corran `build` cada uno**: con 2 slots se bloquean entre sí (uno estuvo
1 h encolado, load 44 sobre 10 cores). En facturaia el `build` ya lo corre el hook `pre-push`, así
que el push no existe sin build verde y el agente no debe repetirlo.
