---
title: un comando dentro de una celda markdown no es un gate
date: 2026-08-03
source: claude-code-session
tags: [gates, harness, markdown, verificacion]
---

Documentar los gates como comandos dentro de una tabla markdown produce gates que parecen
ejecutables y no lo son. Tres fallos reales del mismo origen, en la misma tabla:

- El escapado de `\|` para no romper la celda llega tal cual a la shell, y en ERE `\|` es
  una **barra literal**, no alternancia: el gate anti-secretos no podía coincidir con nada.
  Verde incondicional durante todo su tiempo de vida.
- `python` a secas no existía en esa máquina (solo `python3` y el venv): 127 en cada corrida.
- Una tubería se tragaba el exit code del comando de la izquierda, así que el gate pasaba
  cuando el proceso reventaba.

Los gates van en un `.sh` ejecutable con suite propia; el `.md` describe **qué** miden, no
cómo. Y reservar un tercer código: `0` pasa, `1` falla, **`2` no evaluable** — que nunca
cuenta como verde, porque un gate que no puede mirar no verifica, finge.

Ver [[un-script-gate-con-guard-de-entrypoint-degrada-a-no-op-silencioso]] · [[claude-code-harness]]
