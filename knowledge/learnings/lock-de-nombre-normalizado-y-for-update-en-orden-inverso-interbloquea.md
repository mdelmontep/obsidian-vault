---
title: lock de nombre normalizado y for update en orden inverso interbloquea al renombrar por mayúsculas
date: 2026-10-16
source: agency-portal (pizarra_objective_upsert, PR #851)
tags: [postgres, concurrencia, advisory-lock, plpgsql]
---
Patrón: una RPC de alta por nombre toma `pg_advisory_xact_lock(hash(norm(nombre)))` y LUEGO `for update` de la fila que casa; el renombrado toma `for update` de su fila y LUEGO el lock del nombre nuevo.

Gotcha: si la guarda es textual (`nuevo is distinct from viejo`), «Foo» → «foo» pide `N(foo)` = `N(Foo)`, que tiene ya el alta que espera esa misma fila. Orden inverso → 40P01, que llega crudo y tumba la operación entera.

Fix: tomar el lock (y comprobar duplicados) solo si cambia el nombre NORMALIZADO; si no cambia, ninguna otra fila puede casar con él. Regla general: con dos tipos de lock, el mismo orden en todas las rutas o una guarda que haga imposible el cruce.

Relacionado en el mismo PR: el `exception when raise_exception` de un bloque captura cualquier P0001 (también de un trigger ajeno); usar un SQLSTATE propio (`PZ001`) y capturar solo ese.
