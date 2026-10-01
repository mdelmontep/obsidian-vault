---
title: claude code corta el bash en primer plano con ec=144, y el segundo plano sobrevive
date: 2026-10-01
source: harness ~/.claude (gate-hook.sh), sesiones de facturaia
tags: [claude-code, harness, hooks, gates]
---
- Síntoma: un comando largo (push con pre-push, suite, gate) muere a mitad con `ec=144` (128+16, señal 16), antes de su timeout y sin presión de memoria. 7 casos en una semana; dos de sesiones distintas en el MISMO segundo.
- Los lanzados con `run_in_background` no murieron nunca. No depende del comando, sino del modo.
- Fix en origen, no en prosa: el hook PreToolUse que ya reescribe el comando devuelve en `updatedInput` el `tool_input` entero + `run_in_background:true` + `timeout:7200000` (con los 30 min por defecto un gate en cola moría). `updatedInput` reemplaza el objeto: conservar `description` y el resto.
- Criterio «largo» por el COMANDO (suite completa, gate, build, push con pre-push), no por la clase cpu/mem del semáforo: en un repo ajeno todo es cpu y dura igual.
- Lint, typecheck y vitest de un fichero siguen en primer plano.
- Commit `76c5116` del arnés.
