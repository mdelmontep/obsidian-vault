---
title: un guard caro se criba con la condición necesaria de sus reglas, no con un matcher
date: 2026-09-22
source: claude-harness
tags: [claude-code, hooks, rendimiento, guards]
---
Diez guards en PreToolUse(Bash) sumaban ~1,3 s de CPU por comando y el más lento ~235 ms aunque fuera un `ls`: casi todo era arrancar `python3` (~50 ms) para sacar `tool_input.command` y sanear comillas/heredocs. Los hooks del mismo evento corren en paralelo, así que la espera la marca el MÁS lento: optimizar uno solo no mueve nada.

Fix que no cambia ningún veredicto: extraer con `jq -r '.tool_input.command // empty'` y, antes del saneado caro, salir si falta el texto que TODAS las reglas exigen. Es exacto solo si el saneado nunca CREA texto (quita, o cambia por espacios). Ojo al que BORRA comillas sin dejar espacio: `g''it reset --hard` es `git` para el shell y el saneado lo recompone, así que la criba va por subsecuencia (`*g*i*t*`), no por subcadena (`*git*`). Añadir ese caso a la suite: sin él, la criba equivocada sale verde.

Medido (22-sep): el guard más lento pasa de ~235 a ~75 ms y el CPU total de ~1,3 a ~0,4 s por Bash. Verificación: cada criba mutada a «sale siempre» pone roja su suite, y el guard sin suite se comparó caso a caso contra el original.

Relacionado: [[merge-tree-precheck-cross-pr-y-squash-branch-cleanup]] · [[stop-hooks-lentos-y-routing-de-facturaia]]
