---
title: "`npm run typecheck | tail` enmascara el exit de tsc (el pipeline devuelve el de tail)"
date: 2026-07-17
source: claude-code-session
tags: [ci, typescript, shell, gates]
---
`npm run typecheck 2>&1 | tail -20 && echo OK` ejecuta el `&& echo OK` AUNQUE tsc falle:
el exit de un pipeline es el del ÚLTIMO comando (`tail`=0), no el de tsc. Un gate "verde"
así puede tener errores TS reales sin que te enteres (me pasó: un TS2737 pasó desapercibido).
Fix: captura el exit real → `npm run typecheck > out 2>&1; echo "EXIT=$?"`, o
`grep -qE "error TS" out`. Aplica a cualquier gate (lint/build/test) canalizado a tail/grep/head.
