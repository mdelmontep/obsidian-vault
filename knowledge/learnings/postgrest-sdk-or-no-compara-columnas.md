---
title: postgrest sdk .or() no compara columna contra columna
date: 2026-06-15
source: claude-code-session
tags: [supabase, postgrest, sdk]
---

PostgREST SDK `.or('col_a.lte.0,col_a.lte.col_b')` falla silenciosamente:
el segundo operando se trata como **literal** ("col_b"), no como referencia a columna.

Síntoma: la query devuelve resultados incorrectos o un error de cast.

**Fix**: hacer la query sin el filtro column-to-column y filtrar en memoria:
```ts
const rows = await supabase.from('t').select('col_a, col_b')
const filtrada = rows.filter(r => r.col_a <= 0 || r.col_a <= r.col_b)
```

Alternativa si la tabla es grande: RPC con SQL nativo (`WHERE col_a <= col_b`).

Aplica a `.or()`, `.filter()` y `.eq()` del SDK — ninguno acepta referencias cruzadas.
