---
title: n8n Merge modo combineAll exige que TODOS los inputs conectados reciban datos
date: 2026-08-12
source: claude-code-session
tags: [n8n, merge, gotcha]
---
Un nodo `Merge` con `numberInputs: N` en modo `combine`/`combineBy: combineAll` devuelve **0 items**
si aunque sea UNO de los N inputs conectados nunca se ejecutó (rama de un IF anterior no tomada) —
no es "combina lo que llegó", exige que lleguen todos.

Patrón que lo dispara: fan-out tras un IF donde solo una rama corre en cada ejecución real (ej. "vía
rápida" 1 input vs "vía lenta" 9 inputs) y luego un Merge fan-in con los 10 inputs fijos. La rama
rápida deja 9 inputs sin ejecutar → Merge da `[[]]` → todo lo que sigue (Respond, cierre de tarea)
nunca corre, aunque la ejecución termine en `status:success`.

Fix: usar `mode: "append"` en vez de `combine`/`combineAll` — concatena los items de los inputs que
SÍ llegaron, sin exigir que lleguen todos. Verificado con datos reales: mismo Merge, mismo
`numberInputs`, solo cambiar el modo resolvió el corte (Simarro, cancelación de citas).
