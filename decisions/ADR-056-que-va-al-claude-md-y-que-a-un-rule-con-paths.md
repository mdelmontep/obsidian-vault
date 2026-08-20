---
title: ADR-056 — qué se queda en CLAUDE.md y qué baja a un rule con `paths:`
date: 2026-08-20
status: accepted
tags: [adr, claude-code, harness, contexto]
---

## Contexto

El `CLAUDE.md` se carga entero en cada llamada API y el contexto se relee completo en cada una: 1.000 tokens fijos = 105M de cache-read en 14 días. Cuatro repos tenían bloques enormes de memoria de incidentes ahí (crm 90 KB, tecnocloud 68 KB, facturaia y agh 32 KB). Bajarlos a `.claude/rules/` con `paths:` ahorra, pero un rule condicional **puede no estar** cuando hace falta.

## Opciones consideradas

- **A — Dejarlo todo arriba.** Cero riesgo de que falte; se paga en cada llamada de cada sesión, también las que no tocan el área.
- **B — Bajarlo todo a rules con `paths:`.** Máximo ahorro; pierde reglas en el momento crítico, porque un `paths:` dispara al **leer** un fichero con `Read` (medido: **no** con Bash) y no al ejecutar un comando.
- **C — Reparto por naturaleza de la regla.** Arriba la regla dura en una línea; en el rule el porqué. Más trabajo de redacción y exige criterio explícito.

## Decisión

**C**, con dos criterios que hacen el reparto decidible y no de gusto:

1. **Donde hay un hook determinista que bloquea** (`revoke-guard`, `pre-push` de migraciones, `no-restricted-imports`, un test que fija la prosa), el texto puede bajar: manda el hook, no la prosa.
2. **Donde el momento crítico no lee ningún fichero** que un `paths:` pueda cazar —mergear una PR apilada, desplegar, renumerar una migración justo antes del merge— la regla se queda arriba.

## Consecuencias

Ahorro medido por llamada API: crm −25.7k, tecnocloud −20.2k, facturaia −10.2k, agh −5.3k tokens. Nos compromete a redactar dos veces (regla arriba, porqué abajo) y a comprobar antes de mover: `git check-ignore` del rule, `grep -rl "CLAUDE\.md"` por si un test fija la prosa, y comparación **byte a byte** de que el bloque llegó íntegro. Cerramos como opción el "puntero vacío" — un `CLAUDE.md` que solo diga «ver el rule» deja la regla fuera del 7 % de sesiones que nunca usan `Read`.

Ver [[donde-se-va-el-coste-de-claude-code-no-es-el-claude-md]] · [[claude-code-project-rules-no-se-comparten-si-claude-gitignored]] · [[un-repo-puede-tener-un-test-que-valide-la-prosa-del-claude-md]]
