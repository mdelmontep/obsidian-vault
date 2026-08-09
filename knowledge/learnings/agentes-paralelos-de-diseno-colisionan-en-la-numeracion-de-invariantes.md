---
title: agentes paralelos de diseño colisionan en la numeración y hay que repartir rangos en el prompt
date: 2026-08-09
source: claude-code-session
tags: [claude-code, subagentes, metodo, documentacion]
---
Ocho agentes diseñando áreas distintas de un mismo plan devolvieron invariantes numerados y **tres
eligieron el mismo rango** (`A60`), y dos más chocaron en `M30`. Cada uno miró el máximo existente en el
plan y siguió desde ahí: la colisión es la conducta correcta de cada agente por separado.

Coste real: hay que renumerar al integrar, y las **referencias cruzadas dentro de cada documento** se
renumeran con él, así que el reemplazo tiene que ser por rango y no por búsqueda literal. Se me coló una
cita a `A101` que era `A81` en otro documento.

Fix: **repartir los rangos en el prompt** («tus invariantes son A80-A99, tus gates `G-COP-*`»), igual que
se reparte el fichero de salida. Cuesta una línea por agente y ahorra un pase de integración.

Relacionado: [[3-agentes-paralelos-auditoria-cambios-grandes]].
