---
title: un error de negocio determinista con SQLSTATE 40001 hace que PostgREST lo reintente hasta el timeout
date: 2026-07-27
source: claude-code-session
tags: [postgres, postgrest, supabase, facturaia, rpc, errores]
---

En una RPC llamada vía PostgREST, `RAISE EXCEPTION … USING ERRCODE = '40001'`
(`serialization_failure`) no es un código neutro: PostgREST **reintenta** la
transacción, porque ese código significa "conflicto transitorio, repetir puede
salir bien". Si el error es DETERMINISTA, reintenta hasta que corta el gateway.

Caso TuFacturaIA 2026-07-27. "Marcar cuadrada" y "Marcar presentada" tardaban
**125 s** en fallar cuando el hash de la declaración estaba obsoleto —justo el caso
para el que existe ese guard—, y acababan en `upstream request timeout`. El usuario
veía el botón congelado dos minutos.

La primera hipótesis fue contención de locks (el `SELECT … FOR UPDATE` inicial) y
se aplicó una migración con `lock_timeout = 3s`. **No arregló nada**, porque no era
un lock. Lo que lo delató fue medir por casos en una base sin una sola espera en
`pg_locks` ni `pg_stat_activity`:

```
marcar_cuadrada, id INEXISTENTE  →     266 ms  'declaracion_no_encontrada' (P0002)
marcar_cuadrada, id REAL         → 125.135 ms  'upstream request timeout'
marcar_presentada, id REAL       → 125.123 ms  'upstream request timeout'
fiscal_reabrir, id REAL          →      73 ms  'estado_invalido'   (23514)
recibida_eliminar, id REAL       →     rápido  (409 con su mensaje)
```

Las dos que se cuelgan son EXACTAMENTE las dos que lanzan 40001. Las que responden
al instante usan P0002/23514. Cambiadas a `P0001` conservando el TEXTO del mensaje
(que es el contrato con el endpoint): **125.135 ms → 145 ms**.

Reglas:

- La clase 40 de SQLSTATE es para fallos **transitorios**. Un guard de negocio
  —hash obsoleto, estado inválido, precondición incumplida— es determinista: usa
  `P0001` o la clase 23. Reintentar no lo va a arreglar.
- Un tiempo de respuesta **constante y redondo** (125 s exactos, tres veces) apunta
  a un timeout de infraestructura, no a contención: la contención varía.
- El caso de control lo dio el **id inexistente**: mismo endpoint, misma función,
  respuesta instantánea. Si dos errores de la misma función se comportan distinto,
  la diferencia está en el error, no en la fila.
- Corolario de método: cuando una mitigación no cambia la medición, la hipótesis
  era falsa. Toca decirlo en el propio código (la mig 573 lo dice de la 572) en vez
  de dejar dos arreglos y ninguna explicación.

Ver [[rpc-rls-authuid-vacio-en-service-role]]
