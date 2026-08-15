---
title: el nodo postgres emite success true cuando el returning sale vacío
date: 2026-08-15
source: claude-code-session
tags: [n8n, postgres, idempotencia, gotcha]
---
Patrón habitual de dedup en n8n: `INSERT ... ON CONFLICT DO UPDATE ... WHERE expires_at < NOW()
RETURNING key`, contando con que **0 filas devueltas corten el flujo**. No corta: cuando el
`RETURNING` sale vacío, el nodo Postgres emite `{success: true}` — un item — y todo lo que
viene detrás se ejecuta igual.

El dedup de los avisos de Elphis llevaba así desde que se montó: nunca silenció un solo
mensaje, y parecía correcto porque los avisos llegaban.

Patrón correcto: que la query **devuelva siempre una fila con un booleano**, y que el corte lo
haga el Code siguiente con `return []`.

```sql
WITH upsert AS (INSERT ... RETURNING key)
SELECT EXISTS (SELECT 1 FROM upsert) AS avisar
```

Vale para cualquier gate basado en "no devolvió filas": comprobarlo antes de fiarse.
Ver [[queryreplacement-trocea-por-comas-todo-valor-que-no-sea-json]] · [[ejecucion-en-verde-no-prueba-el-efecto]]
