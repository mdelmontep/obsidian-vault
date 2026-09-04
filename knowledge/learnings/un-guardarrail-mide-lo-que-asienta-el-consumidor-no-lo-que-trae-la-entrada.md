---
title: un guardarraíl mide lo que va a asentar el consumidor, no lo que trae la entrada
date: 2026-09-04
source: facturaia
tags: [guardarrail, postgres, stock, revision]
---

Un gate que valida un valor tiene que calcularlo **igual que lo va a calcular quien lo
consume**. Si lo mide de la entrada cruda, falla en las dos direcciones: bloquea lo que
nunca llega al destino y calla ante lo que sí llega.

Caso (FacturaIA, ticket #171, mig 828): el guardarraíl de coste anómalo de la aprobación
pasaba `lineas_factura.precio_unitario` tal cual. El ledger de stock asienta otra cosa:
`round(media_ponderada_por_catalogo_id * tipo_cambio, 4)`. Dos defectos de un solo error —
en una recibida en yenes el aviso saltaba **siempre** (comparaba yenes contra un histórico
en euros), y con el mismo producto en dos líneas a precios distintos bloqueaba sobre un
número que no existe en el almacén. Fix: copiar el `SELECT` del asiento letra por letra,
incluidos sus filtros, y quedarse solo con los que cambian el número.

Los encontró un `/code-review` con dos subagentes, no los tests: la suite del PR estaba
verde porque medía la forma del SQL, no su equivalencia con el consumidor.
