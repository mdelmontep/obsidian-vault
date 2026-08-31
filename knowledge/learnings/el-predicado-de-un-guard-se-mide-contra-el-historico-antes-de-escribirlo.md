---
title: el predicado de un guard se mide contra el histórico de prod antes de escribirlo
date: 2026-09-01
source: facturaia
tags: [guards, sql, migraciones, produccion, datos]
---

Un albarán con líneas sin producto se validaba igual y cerraba el documento vacío: el género no entraba en el inventario y `validado` es terminal. El guard es obvio; **el predicado no**.

El agente de diseño propuso vetar lo que el propio asiento usa para resolver el producto: `COALESCE(al.catalogo_id, m.catalogo_servicios_id) IS NULL`. Parece el predicado canónico —es el que el código ya escribe— y por eso es la trampa. **Medido antes de escribirlo, habría rechazado 9.567 albaranes YA VALIDADOS** de una sola org: ahí la línea viene de un pedido con `material_id` y el material sin enlazar al catálogo es el estado normal — el material identifica el producto aunque no controle stock.

El predicado correcto es el estrecho, `catalogo_id IS NULL AND material_id IS NULL`. Con él la medición sobre prod devuelve **el bug y nada más**: 25 líneas, 7 albaranes, todos `abierto`, todos de un único cliente, cero validados.

Método, y vale para cualquier CHECK, guard o gate nuevo sobre datos vivos: **antes de escribir el predicado, córrelo como `SELECT` contra el histórico completo y mira a cuántas filas YA CERRADAS habría dicho que no**. Si el número es grande, no has encontrado un bug: has escrito mal la regla. La expresión que el código usa para *resolver* no es la misma que debe usar para *exigir*.

Ver [[medir-alcance-en-multi-tenant-sin-agrupar-por-org-mezcla-la-sandbox]] · [[convertir-columna-en-derivada-exige-backfill-del-historico]] · [[el-candado-audita-la-clase-no-la-lista-que-alguien-escribio]]
