---
title: una migración aplicada sin registrar hace mentir a `migration list`, y ningún guard que compare máximos la ve
date: 2026-09-06
source: claude-code-session facturaia
tags: [supabase, migraciones, schema-migrations, guard, verificacion, gotcha]
---
Base local compartida por siete worktrees. Una sesión aplicó su migración con
`supabase db query --file` para medir sin ocupar número todavía — vía legítima, pero **que
no registra**. Resultado: el catálogo la tenía y `supabase_migrations.schema_migrations` no.

Dos sesiones diagnosticaron lo contrario y **las dos midieron bien**: una consultó el registro
(«no está aplicada»), otra recordaba haberla aplicado. Lo único que discriminó fue
`pg_get_functiondef` sobre **una función concreta**. Coste colateral: mi push pasó a verde tras
tres rojos porque el arreglo estaba operando sin que ningún árbol lo declarase.

**Registro y catálogo son dos preguntas distintas.** Para afirmar «esto está aplicado» hacen
falta las dos: `select max(version) from supabase_migrations.schema_migrations` **y** el objeto
en `pg_get_functiondef` / `information_schema`.

Corolario para guards: **comparar «último registrado» con «último aplicado» no discrimina**, porque
el esquema no lleva número — no hay «último aplicado» que consultar. En este caso el máximo
registrado seguía siendo el correcto con la migración fantasma ya viva. Un guard así da verde
justo en el caso peligroso. Lo honesto es que **declare su ceguera** («comparo el registro con el
disco de esta rama; no veo DDL aplicado sin registrar») en vez de prometer «al día».

Y la otra mitad, el mismo día: `supabase migration list --linked` compara prod contra el
directorio `supabase/migrations/` **del cwd**, no contra la rama que crees. Desde el checkout
principal (58 ficheros por detrás) reportó 58 divergencias fantasma. Comprobación en positivo, que
no se puede leer al revés: `git merge-base --is-ancestor origin/main HEAD`.

Caso «registrado sin ejecutar», el inverso, en
[[un-bootstrap-que-aplica-el-estado-final-sin-registrar-los-pasos-hace-que-el-migrador-los-repita]].
Familia «la herramienta mide el árbol que le pones delante»:
[[un-comando-de-reparacion-corrido-desde-un-checkout-viejo-repara-a-la-version-vieja]].
