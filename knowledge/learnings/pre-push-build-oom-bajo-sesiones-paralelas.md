---
title: pre-push que corre build muere por OOM bajo sesiones paralelas — pushea en ventana libre, nunca --no-verify el build
date: 2026-07-16
source: claude-code-session
tags: [claude-code, worktree, git-hooks, build]
---
Si el hook pre-push corre `npm run build` (gate) y varias sesiones/worktrees
corren `next build` a la vez, macOS jetsam mata tu build (y los hooks node del
pre-commit = eslint/tsc): commit/push fallan con estado "killed", output vacío,
compile Turbopack ✓ pero muere en "Running TypeScript". NO es tu código.
Diagnóstico: `ps aux | grep "next build" | grep -v <tu-worktree>`; si hay ≥2,
ESPERA a la ventana libre (0-1 ajenos) y pushea (build ~15-55s cuando libre).
Táctica: monitor ligero (ps/vm_stat) que avise cuando 0 ajenos; separa la espera
(ligera, sobrevive) del push (pesado). NUNCA saltes el gate de build con
`--no-verify` (build es la verdad). `--no-verify` solo justificable en el
pre-COMMIT (si lint/typecheck ya se verificaron aparte, verdes), jamás en el
build del pre-push. Ver [[actions-sin-billing-hooks-locales-unico-gate]].

Corolario (2026-07-16): bajo la misma saturación, `npm test` completo puede dar
FALSOS fallos por timeout de test (5s) en ficheros que no tocaste — no asumas
regresión: reejecuta ese fichero aislado (`npx vitest run <ruta>`); si pasa
limpio en 1-2s, era carga de CPU, repite la suite completa una vez más antes
de comitear.

Matiz (misma sesión, caso distinto): si YA corriste `rm -rf .next && npm run
build` en foreground hasta el final (exit 0, output completo, no solo
typecheck) momentos antes, `--no-verify` en el push SÍ es seguro y
documentable — no estás saltando el gate, ya lo pasaste tú mismo por fuera del
hook. La prohibición de arriba aplica cuando NO has verificado el build de
forma independiente y usas `--no-verify` solo para "salir del paso" sin saber
si compila. Ver [[worktree-facturaia-build-supabase]] (mismo patrón, doc previa).
