---
title: convertir una columna en derivada exige backfill del histórico, o dejas minas
date: 2026-08-06
source: claude-code-session facturaia
tags: [postgres, migraciones, bd, backfill, produccion]
---

Cuando una migración pasa a DERIVAR una columna de una tabla de eventos, arregla
el futuro y deja armado el pasado: las filas que ya tenían el valor escrito a mano
no tienen evento detrás, así que el primer recálculo las pone a cero **en silencio**.

Caso TuFacturaIA (mig 640 → 644): el ledger `factura_pagos` hizo de
`facturas.estado` una columna derivada. Las cobradas de antes no tenían fila:
**15 de 15 pasaron `cobrada` → `pendiente` con `fecha_cobro` a NULL** al recomputar,
sobre 1.385 de 1.403 (98,7%). Lo dispara cualquier trigger de la tabla de eventos.
Y el daño no es la etiqueta: `fecha_cobro` alimentaba cashflow, KPI y base caja.

- **Censo antes de escribir la migración**: `count(*)` de filas con el estado que
  la columna afirma y CERO evidencia en la tabla de eventos. Si no es 0, hay minas.
- El backfill inserta el evento que falta con un `origen`/`nota` propio
  (`'importado'` + `nota='backfill-mig-NNN'`) → reversible con un `DELETE … WHERE nota=`.
- Importe/valor a insertar: pedirlo a **la misma función que usa el recompute**, no
  a una resta escrita en la migración, o discrepan por céntimos.
- **La verificación es volver a derivar y comprobar que nada se mueve.** Contar
  filas insertadas no prueba nada. Ver [[verificar-un-backfill-con-el-predicado-que-lo-filtro-se-valida-a-si-mismo]].
- Descartar el guard «si no hay evidencia no la toques»: perpetúa N filas sin
  respaldo, que es el estado invisible que la migración venía a eliminar.

Continuación de [[columna-derivada-por-recompute-solo-admite-un-escritor]].
