---
title: withApiAuth solo carga `role` si el endpoint declara requireRole/requireWrite
date: 2026-06-16
source: claude-code-session
tags: [facturaia, auth, gotcha]
---

En TuFacturaIA, `withApiAuth` (`src/lib/api/with-api-auth.ts`) hace el lookup de
`role` SOLO cuando `opts.requireRole` u `opts.requireWrite` están set
(`needsRoleLookup`). Si el endpoint no declara ninguno, el handler recibe
`role = null` aunque el usuario tenga rol real.

Trampa: cualquier lógica dentro del handler que dependa de `role`
(p. ej. `if (role && SEED_ROLES.has(role)) { seed }`) se convierte en **código
muerto** — nunca corre, sin error visible. Caso real: el seed de
`categorias_contables` en `GET /conciliacion/categorias` no declaraba requireRole
→ role=null → 5/6 orgs reales sin categorías; el modal "Registrar como ingreso"
y el desplegable de clasificación salían vacíos (fix PR #278 + mig 301 backfill).

Segundo caso (2026-06-19): `GET /series` devolvía `can_manage: role === 'propietario'`
→ role=null → botones editar/eliminar ocultos para todos aunque el usuario fuera
propietario. Fix: `canActorDoAction('series.manage')` en el handler en paralelo
con la query DB, mismo patrón que PATCH/DELETE del mismo archivo.

Fix/patrón: NO dependas de `ctx.role` en un GET sin requireRole/requireWrite.
O lo declaras, o haces el lookup explícito en el handler (vía `canActorDoAction`),
o (si la acción es inocua e idempotente, como sembrar defaults) la haces sin gate.
Ideal: documentarlo en `docs/architecture/gotchas.md §Auth`.
