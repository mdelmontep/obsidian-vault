---
title: una columna deprecada con un comentario conserva sus índices y sigue rechazando inserts
date: 2026-08-03
source: claude-code-session
tags: [postgres, ddl, migraciones, antipatron]
---

Marcar una columna como deprecada en un comentario **no la desactiva**: conserva sus
índices, sus `UNIQUE` y sus `CHECK`. Una columna que nadie escribe sigue pudiendo
**rechazar un `INSERT`**, y eso no se ve leyendo el código de la aplicación porque en el
código ya no aparece.

Caso real leído en Dolibarr (20 años en producción): `llx_societe.prefix_comm varchar(5)
-- prefix commercial (deprecated)` con `ALTER TABLE … ADD UNIQUE INDEX
uk_societe_prefix_comm(prefix_comm, entity)` **vivo**. Y en la misma tabla, `statut
-- (deprecated)` conviviendo con `status` cuatro líneas más abajo: dos columnas para un
hecho, dos décadas, porque nadie se atreve a borrar la primera.

Regla: **una columna no se deprecia, se borra**, y el motivo va en la prosa de cabecera
de la migración que la borra — no en un comentario junto a la columna que se queda.

Gate (TuCRMIA, `scripts/mig-check.mjs`, `findColumnasDeprecadas`): prohíbe el marcador
`deprecated|deprecado|obsoleto|unused` en la línea de una definición de columna, un
`add column` o un `comment on column`. **Deja pasar** la prosa de cabecera y el
`drop column` con su motivo al lado — un gate que falla sobre trabajo correcto enseña a
saltárselo.
