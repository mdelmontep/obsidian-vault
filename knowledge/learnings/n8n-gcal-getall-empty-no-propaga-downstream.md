---
title: n8n Google Calendar getAll vacío no propaga a nodos downstream
date: 2026-05-25
source: claude-code-session
tags: [n8n, google-calendar, gotcha]
---

Si `Google Calendar > Get Many Events` devuelve 0 eventos (franja libre), n8n NO ejecuta nodos downstream — la rama muere silente. Esto rompe pattern habitual "consultar disponibilidad → si vacío respond 'libre'".

Fix con dos cambios:
1. Setear `alwaysOutputData: true` en el nodo GCal → emite item vacío en lugar de 0 items.
2. En el Code node downstream, filtrar el item placeholder:
```js
const events = $input.all().filter(e => e.json && e.json.start);
```
Sin el filter, `e.json.start.dateTime` crashea con TypeError porque `e.json.start` es undefined en el placeholder.

Caso real: EcoBox `Mirar_disponibilidad` 2026-05-25 — el primer fix `alwaysOutputData` solo no era suficiente; necesitaba el filter en `Format slots`.
