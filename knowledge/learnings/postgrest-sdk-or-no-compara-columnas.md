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

**Fix preferido si la comparación es un filtro frecuente**: columna generada `STORED` booleana (`en_alarma bool GENERATED ALWAYS AS (controla_stock AND stock_actual<=stock_minimo) STORED`) → filtrable con `.eq('en_alarma', true)` + índice parcial. Una sola fuente para endpoint, cron e índice. Ver [[columna-generada-stored-para-equivalente-derivado]].

**Footgun del fix en memoria**: si limitas (`.limit(N)`) ANTES de filtrar en JS, descartas filas que sí cumplían → falsos negativos. Caso real: cron alarmas stock 2026-06-16 (`limit(BATCH*4)` + filtro JS dejaba productos en alarma sin notificar).

Aplica a `.or()`, `.filter()` y `.eq()` del SDK — ninguno acepta referencias cruzadas.

**`now()` tampoco se puede expresar** en un `.update({ col: 'now()' })`: viaja como literal JSON, así que sellarías el reloj de Node, no el de Postgres. Combinado con lo de arriba, un **claim atómico** («marca la fila si venció su intervalo, y devuélvemela») no es expresable desde el SDK: `where last_run_at < now() - make_interval(mins => interval_minutes)` es a la vez `now()` y columna-contra-columna. Va como RPC `security definer` con `for update skip locked` (patrón `claim_next_feedback_ai_job`, agency-portal). Comprobar-y-luego-marcar en dos llamadas deja pasar dos ejecuciones simultáneas.
