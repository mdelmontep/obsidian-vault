---
title: n8n postgres node con webhook lastnode solo devuelve primer row
date: 2026-05-22
source: claude-code-session
tags: [n8n, postgres, webhook]
---

Webhook con `responseMode: lastNode` después de un Postgres `executeQuery` que devuelve N filas solo retorna la **primera fila** en la respuesta HTTP. n8n trata cada row como un item separado y `lastNode` colapsa al primero.

Síntoma: `SELECT tablename FROM pg_tables WHERE schemaname='public'` devuelve solo `ai_builder_temporary_workflow` aunque haya 78 tablas. Engaña pensando que las queries previas no se ejecutaron.

Fix: agregar a una sola fila con SQL:
```sql
SELECT array_agg(tablename ORDER BY tablename) AS tablas
FROM pg_tables WHERE schemaname='public'
-- o
SELECT json_agg(row_to_json(t)) FROM (...) t
```

Alternativa: cambiar `responseMode` a `responseNode` y usar un nodo `Respond to Webhook` con `responseBody: {{ JSON.stringify($items()) }}`.

Caso real: EcoBox 2026-05 — pensé que el CREATE TABLE no había corrido porque verify solo mostraba una tabla.
