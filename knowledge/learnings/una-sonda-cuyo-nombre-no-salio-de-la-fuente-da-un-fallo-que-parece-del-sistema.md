---
title: una sonda cuyo nombre no salió de leer la fuente da un ✗ que parece un fallo del sistema
date: 2026-08-31
source: tucrmia
tags: [verificacion, migraciones, supabase]
---
Tras aplicar 29 migraciones a producción, la comprobación contra el catálogo de PostgREST devolvió
tres ✗: `sweep_stale_leases`, `reemitir_enlace_de_acceso` y `crm_ficheros_insert`. Se leen como
«tres migraciones no entraron». No faltaba ninguna: los tres nombres me los había inventado yo —el
real era `stale_lease_sweep`.

Y no fue casualidad: los tres fallos eran **exactamente** los tres nombres que NO había sacado de
leer el `create function` de su fichero. Los que sí, todos verdes.

Fix: la lista de sondas se **deriva** de la fuente (`grep -oE 'create (or replace )?function [a-z_]+'`),
nunca de memoria. Una sonda escrita a mano comparte modo de fallo con lo que vigila, y su ✗ es
indistinguible de un fallo real: el peor tipo de falso negativo, porque invita a «arreglar» algo que
está bien. Ver [[un-control-negativo-que-no-discrimina-invalida-el-test-entero]].
