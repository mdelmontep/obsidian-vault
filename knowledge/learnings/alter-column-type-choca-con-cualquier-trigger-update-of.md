---
title: ALTER COLUMN TYPE choca con cualquier trigger que nombre esa columna
date: 2026-08-07
source: claude-code-session
tags: [postgres, migraciones, triggers]
---

`ALTER TABLE ... ALTER COLUMN x TYPE ...` falla con *«cannot alter type of a
column used in a trigger definition»* si algún `CREATE TRIGGER ... UPDATE OF x`
la nombra. No lo dice ninguna guía de migración: sale al aplicarla.

El arreglo es soltar los triggers y recrearlos, pero **captúralos del catálogo
con `pg_get_triggerdef`, nunca copies el texto de su migración original**: en un
repo vivo los redefinen por el camino. Aquí,
`trg_obras_recalcular_por_material_update` nació con 2 columnas y hoy lleva 6;
recrearlo desde la migración vieja lo habría dejado mutilado y el precio dejaría
de recalcularse **sin que nada fallara**.

Y mira qué hace cada trigger antes de recrearlo: uno de ellos regeneraba el
desglose congelado de las líneas contra el catálogo de hoy, así que tenía que
volver DESPUÉS de la conversión, no antes.

Detectarlos: `pg_get_triggerdef(t.oid) ~* 'UPDATE OF[^)]*\m(col1|col2)\M'`.

Relacionado: [[postgres-rpc-firma-identica-create-replace]]
