---
title: reescribir una función vieja la somete a los guards de hoy, y ahí sale su deuda
date: 2026-09-20
source: facturaia
tags: [sql, postgres, supabase, hooks, migraciones, seguridad]
---

Copiar una función verbatim con `CREATE OR REPLACE` para cambiarle UNA línea no es
neutral: el fichero vuelve a pasar por los guards que no existían cuando se escribió.
Eso trae dos cosas a la vez, y conviene saber cuál es cuál.

- **Lo que el guard pide y es ruido**: `REVOKE ALL` vs `REVOKE EXECUTE`, grants que
  otra migración ya cambió. Se copia el original y el hook para el commit.
- **Lo que el guard pide y es un BUG vivo**: en facturaia (mig 922) el `pre-push`
  señaló que `fiscal_calcular_cuadres` llamaba a `user_can_write_in_org` sin
  condicionar a `auth.uid() IS NOT NULL`. Medido contra la base local: con la service
  role key `auth.uid()` es NULL, no hay fila en `org_members` y la función abortaba con
  `42501` en TODAS sus llamadas desde la mig 150. Su único llamador se tragaba el error.

Regla: cuando un guard dispare sobre código que solo estás COPIANDO, mídelo antes de
copiar el original tal cual — no asumas que es ruido histórico. Y arréglalo en la misma
migración si tu cambio depende de que esa función funcione, o entregas letra muerta.
Ver [[filtro-texto-libre-a-columna-tipada-error-tragado-parece-vacio-real]].
