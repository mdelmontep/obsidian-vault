---
title: el statement_timeout lo fija authenticator y no se rearma dentro de plpgsql
date: 2026-09-05
source: facturaia
tags: [postgres, supabase, postgrest, timeout]
---

Medido el 5-sep-2026 en facturaia, idéntico en prod y en local. Dos cosas, las
dos al revés de lo que parece:

**El techo de una RPC con service key lo pone `authenticator`, no `service_role`.**
PostgREST conecta siempre como `authenticator` y luego hace `SET ROLE`, así que
manda su `proconfig` (`statement_timeout=8s`, `lock_timeout=8s`) aunque el de
`service_role` esté vacío. Mira el `proconfig` de los cuatro roles antes de
concluir "no hay límite".

**Trocear dentro de PL/pgSQL no rearma el reloj.** Se arma en la sentencia de
nivel superior y las anidadas no lo reinician: no lo rearman ni el `proconfig` de
la función ni un `SET LOCAL` en el cuerpo. Solo un `SET LOCAL` en una sentencia
PREVIA de la misma transacción, inalcanzable desde `supabase-js`.

Así que ante «esto roza el timeout»: medir primero (la tanda de 2.000 tardaba
378 ms contra 8.000 de techo) y, si hace falta, trocear DESDE EL CLIENTE.
