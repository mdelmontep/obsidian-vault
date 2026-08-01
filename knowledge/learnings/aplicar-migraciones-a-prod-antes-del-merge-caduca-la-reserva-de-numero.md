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
