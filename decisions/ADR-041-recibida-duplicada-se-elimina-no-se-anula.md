---
title: ADR-041 — una factura recibida duplicada se elimina, no se anula
date: 2026-07-26
tags: [decisions, facturaia, fiscal]
---

## Contexto

Al conectar la detección de duplicados de recibidas (FacturaIA, `ingesta-001`) hacía
falta darle salida al usuario: 8 grupos con copias en estado contable duplicaban
**532,20 € de IVA soportado** y no existía ninguna acción para arreglarlo.

## Opciones

1. **Estado nuevo `duplicada`** para recibidas, excluido de los agregados.
2. **Eliminar** la factura, con bloqueos por consecuencia contable.
3. Reutilizar `anulada`.

## Decisión: (2) eliminar

- (3) queda descartada por dato, no por gusto: `ESTADOS_RECIBIDA_FUERA` solo excluye
  `sin_aprobar` y `disputada`, así que una recibida `anulada` **seguiría contando en
  el 303** —no arreglaría nada— y dispararía el cuadre C-05 "anulada sin abono",
  que en la factura de un proveedor no significa nada.
- (1) añade un concepto al dominio para nada: una recibida es NUESTRO registro de la
  factura de otro. No la emitimos, así que no hay nada que anular ni rectificar (el
  abono lo emite quien facturó). Lo que existe es un apunte que no debería, y lo que
  se corrige son nuestros libros.
- Es lo que hace el sector. Holded: un gasto mal introducido se borra (Remove, con
  papelera de 10-30 días), sin estado "duplicado" y sin anular; el único bloqueo es
  el **periodo fiscal cerrado**, porque borrar el pago borraría el asiento.

## Consecuencias

- Los bloqueos ya estaban en el esquema como FK RESTRICT (snapshot fiscal, stock,
  SEPA, recordatorios): no había que inventarlos, había que traducirlos a mensajes
  con salida. Pero sí distinguir estados, ver
  [[fk-restrict-no-sirve-como-regla-de-negocio-no-distingue-estados]].
- La papelera es la fila de `bandeja_ingesta`: se desliga y se marca `descartado`,
  el documento y sus `datos_extraidos` se conservan y desde ahí se puede volver a
  aprobar.
- Se arrastra la conciliación bancaria, mismo criterio que Holded al borrar el pago
  con el gasto. Detalle que lo obliga: la FK cuenta también las asignaciones
  desvinculadas (el desvinculado es soft), así que desvincular no libera el borrado.
- Cambia el inviolable de `CLAUDE.md`: recibidas se eliminan en cualquier estado;
  emitidas siguen solo en `borrador` (RD 1619/2012).
