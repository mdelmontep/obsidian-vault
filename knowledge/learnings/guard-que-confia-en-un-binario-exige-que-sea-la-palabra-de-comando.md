---
title: un guard que confía en un binario por nombre exige que sea la palabra de comando
date: 2026-10-16
source: agentesia-skills#32 (guard de fuentes de la Pizarra), retro 16-oct
tags: [hooks, seguridad, claude-code]
---
Un hook PreToolUse que deja pasar `vault-commit …` por nombre y revisa sus argumentos se rodea con un lanzador que añade argumentos que el guard no ve: `xargs`, `parallel ::: …`, `find -exec`, `timeout`, `sudo`, `sh -c`, `bash`, `rg --pre` y subcomandos de git que ejecutan (`bisect run`, `rebase -x`, `-c alias.x='!…'`, `submodule foreach`).

Patrón:
- Confianza solo si el binario es la PRIMERA palabra del comando simple; nombrado en otra posición → deny, salvo verbos que solo lo leen (`cat`, `git diff`).
- Una lista de «verbos lectores» no puede incluir `git` entero: solo sus subcomandos de datos.
- Rutas de flags que escriben: relativas y sin `..`.
- Una asignación `X=…` cuenta solo en posición de comando (`--from hot=/tmp/x` no es entorno).
- Tests de deny por lanzador + mutantes de la función que decide.
- Ni «palabra mágica» en el texto: `dokploy-secret-guard` eximía todo comando con `dokploy-safe` (`curl … # dokploy-safe`); una inyección la escribe igual. Quitarla si la forma legítima ya pasa por otra condición (17-oct).

Relacionado: [[claude-code-gotchas]]
