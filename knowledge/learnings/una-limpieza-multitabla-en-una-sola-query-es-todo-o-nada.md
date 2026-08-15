---
title: una limpieza multi-tabla en una sola query es todo-o-nada, y su aviso por stderr no es un fallo
date: 2026-08-11
source: claude-code-session
tags: [supabase, postgres, testing, smoke, tucrmia]
---
El `teardown` de un smoke que borra 15 tablas hijas + la padre en **una sola** llamada
(`/database/query` de la Management API, o un `psql` multi-sentencia) corre en UNA transacción:
si la última falla por `23503`, **se deshacen las quince anteriores** y no se borra nada.

Caso real (TuCRMIA, 11-ago): una migración añadió `product_events` con FK a `organizations` y
nadie la puso en `limpiar()`. Desde ese día **cada corrida** —verde o roja— dejó en producción
2 organizaciones, 1.009 leads, 2.223 filas de registro y 38 credenciales. Meses de residuo.

Lo que lo hizo invisible no fue el bug, fue el **canal del aviso**: el `catch` imprimía por
`stderr` ANTES de las 62 líneas de ✓, el `exit code` seguía siendo 0, y la última línea decía
«datos de prueba borrados» de forma incondicional — el guion desmentía su propio aviso.

**Fix del patrón, no del caso**: la limpieza es una COMPROBACIÓN más, con su ✓/✗ y su peso en el
código de salida — tras borrar, preguntar a la base si queda algo (`select count(*) … where id in
(…)`). Así la tabla nº16 que alguien añada pone el smoke en rojo la primera vez que se ejecute.
Alternativa sin teardown: [[smoke-prod-en-transaccion-rollback]].

**Volvió el 14-ago en el smoke hermano, con `outbox_events`** — mover una tarjeta encola una fila,
que es lo único que ese smoke hace. Mil leads en producción y «Datos de prueba borrados». La
lección nueva no es el mecanismo: es que **arreglar un guion no arregla a sus hermanos**, y aquel
arreglo se quedó donde se escribió. A la segunda vez no toca parche sino **gate**: uno que exija
por árbol de sintaxis que cada `smoke-*` llame a su limpieza y que DESPUÉS relea la base y pase el
resultado por la comprobación. Al encenderlo señaló 2 de 3.
Ver [[dos-trampas-al-escribir-un-gate-por-arbol-de-sintaxis]]
