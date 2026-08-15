---
title: verificar rls sobre una tabla vacía no discrimina — mete una fila antes
date: 2026-08-15
source: claude-code-session
tags: [supabase, rls, verificacion, postgrest]
---

Tabla nueva con `ENABLE ROW LEVEL SECURITY` y sin políticas. Con la anon key,
PostgREST devuelve `200 []`. Parece que RLS aísla — pero la tabla está **vacía**,
así que `[]` es lo que devolvería igualmente sin RLS. La comprobación no mide nada.

Discrimina así: inserta una fila con `service_role`, y entonces compara.

```
service_role → 1 fila     anon → 0 filas     ← ahora sí prueba algo
```

Mismo patrón para el índice único parcial (`WHERE estado <> 'terminado'`): el
segundo insert debe dar `23505`, y tras marcar la fila `terminado` el insert debe
entrar. Sin las dos mitades solo sabes que "no falló".

Generalización: **toda verificación cuyo resultado esperado sea "vacío" hay que
correrla también en el estado donde debería salir NO vacío.** Si no, el verde
puede venir de que no hay nada que ver. Ver [[feedback_no_verificar_readonly_escribiendo]]
para el reverso (no verificar solo-lectura escribiendo a ciegas).
