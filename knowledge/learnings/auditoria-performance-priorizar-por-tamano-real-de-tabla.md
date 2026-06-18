---
title: auditoría de performance bd — priorizar por tamaño real de tabla, no por el patrón abstracto
date: 2026-06-18
source: claude-code-session
tags: [postgres, supabase, performance, auditoria, metodo]
---

Antes de "arreglar" hallazgos de performance (N+1, falta de paginación, índices),
consultar el **tamaño real**: `pg_stat_user_tables` (`n_live_tup`) +
`pg_total_relation_size`. En apps jóvenes la mayoría de bottlenecks son
**latentes**: un seq scan sobre 70 filas es instantáneo, así que el "arreglo"
es preventivo, no urgente.

Caso FacturaIA 2026-06-18: tablas de negocio diminutas (facturas 123, líneas 70,
movimientos 73) y muy bien indexadas; el dolor real estaba donde el patrón
abstracto no mira — las tablas de log (ver [[tablas-de-log-sin-retencion-dominan-el-tamano-de-la-bd]]).

Método: cruzar tamaños reales + `pg_indexes` ↔ filtros del código ANTES de tocar.
Y ser honesto en el informe: separa "ya duele" de "escala mal en el futuro".
Repartir la auditoría en agentes por categoría funciona, pero ~50% son falsos
positivos → filtrar contra el esquema real. Ver [[supabase-errores-que-solo-afloran-contra-schema-real]].
