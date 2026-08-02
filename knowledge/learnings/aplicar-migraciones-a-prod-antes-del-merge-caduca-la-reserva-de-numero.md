---
title: aplicar migraciones a prod antes del merge caduca la reserva de número
date: 2026-08-01
source: claude-code-session
tags: [supabase, migraciones, deploy, incidente, facturaia]
---

Un agente aplicó 6 migraciones a prod para poder tomar capturas. Antes de ramificar
verifiqué que ninguna rama viva usaba esos huecos: era cierto, y **caducó en dos horas**.
Otro PR mergeó su propia `607` y prod ya la tenía anotada con MI contenido → el siguiente
`db push` la habría dado por aplicada y **saltado en silencio** (8 orgs, 5 de clientes
reales, sin poder dar de alta 2ª empresa, con el deploy diciendo OK).

- El número se asigna **justo antes del merge** no por burocracia: porque "lo he
  comprobado" tiene fecha de caducidad mientras la rama vive.
- Lo paró el hook de `pre-push`, no una revisión humana. Cuarta vez que lo para él.
- **Reparar** (nunca editar `schema_migrations` a mano): `migration repair --status
  reverted <viejos>` y `--status applied <nuevos>`. El `reverted` corre desde cualquier
  checkout; el `applied` **exige los ficheros presentes**, así que hay que lanzarlo desde
  el worktree renumerado, copiándole `supabase/.temp/` entero (solo `project-ref` da
  `LegacyDbConfigIpv6Error`).
- Si el CLI pide `SUPABASE_DB_PASSWORD`: `op read` inline, no exportar.

Complementa [[migracion-numerar-contra-prod-schema-migrations]] (allí prod va por delante
por ramas ajenas; aquí la divergencia la causé yo).

**El otro lado de la misma regla (02-ago)**: aplicar antes cuida el NÚMERO, pero el
esquema hay que aplicarlo antes por otro motivo — **el código desplegado lo exige**.
Mergeé dos PRs y dejé el `db push` para el final; entre medias se cayó el pooler y prod
quedó llamando a una RPC inexistente → `/api/obras/materiales/familias` en 500. Hubo que
revertir los dos PRs. Orden bueno: `db push` → `migration list` para confirmar → merge.
Un `db push` que falla es razón para **parar el merge**, no un paso que se apunta para
luego. Y ojo con el orden inverso: el número se renumera justo antes de cada merge, así
que en una tanda de varios PRs con migración toca ir de uno en uno.
