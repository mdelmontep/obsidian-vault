---
title: Un precio unitario de 1,00 marca una cantidad que en realidad son euros
date: 2026-08-07
source: TuFacturaIA · coste/hora de instalador en el ERP WAPI de IET
tags: [learning, datos, unidades, erp, medicion]
---

En la tabla de partes de trabajo de WAPI, cada línea lleva horas y el precio/hora
congelado. Al sacar la media ponderada del coste salían **1,00 €/h en 2025** y
cifras absurdas casi todos los años.

La causa: cuando meten **subcontrata**, ponen el importe en la columna de horas y
el precio a **1,00**. La columna deja de ser horas y pasa a ser euros, sin marca
de ningún tipo. En 2022-23 eran **38 líneas con 53.111 «horas»** — 1.400 h por
línea, imposible — contra 451 líneas reales con 25.361 horas de verdad.

**El patrón**: en cualquier ERP, un precio unitario de 1,00 es el truco universal
para meter un importe por una columna de cantidad. Antes de promediar
`SUM(cant*precio)/SUM(cant)`, mirar el reparto por precio y excluir el 1,00.

**Cómo se detecta sin conocer el ERP**: agrupa por precio y ordena por volumen.
La fila contaminada canta sola — concentra la mayoría del volumen en un puñado de
líneas con el precio más redondo posible.

Relacionado: [[dos-piezas-en-la-misma-unidad-equivocada-dan-el-resultado-correcto]] ·
[[agregar-sobre-todas-las-orgs-mezcla-datos-sembrados-con-datos-de-cliente]]
