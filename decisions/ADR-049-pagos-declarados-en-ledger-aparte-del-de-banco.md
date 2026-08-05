---
title: ADR-049 — los cobros declarados van a un ledger aparte del bancario
date: 2026-08-06
status: aceptada
tags: [adr, facturaia, bd, conciliacion]
---

# Contexto

`facturas.estado` tenía dos escritores: la vía bancaria, donde
`movimiento_factura_asignacion` es el evento y `recompute_factura_estado` deriva
el estado; y el marcado manual (más la confirmación del cliente por WhatsApp),
que escribía `estado` a pelo sin dejar fila. Como recompute recalcula desde cero
y pisa, un cobro manual desaparecía al vincular y desvincular un movimiento.

# Alternativas

1. **Un solo ledger** que absorba también las asignaciones bancarias. Correcto en
   teoría, pero obliga a que la mitad de las columnas y TODOS los guards
   (sobre-cobro mig 133, capacidad del movimiento mig 265, devoluciones,
   anticipos, restos) pasen a ser condicionales.
2. **Columnas en `facturas`** para el pago manual. No soporta pagos parciales de
   fuentes mixtas y deja el estado sin derivar.
3. **Ledger aparte** (`factura_pagos`) solo para pagos sin movimiento detrás.

# Decisión

La 3. Partición por naturaleza del hecho: un cobro bancario tiene extracto e
invariantes propias, uno declarado no tiene ninguna de las dos. Lo que sí se
unifica es la LECTURA — `factura_cobros_resumen` (mig 641) es la única suma, y
`recompute_factura_estado` la llama en vez de repetirla.

# Consecuencias

- recompute pasa a ser el único escritor de `estado`; nadie más lo toca.
- `factura_pagos.importe_eur` va en la escala del TOTAL FISCAL, que es contra lo
  que compara recompute. Con `importe_cobrable` y IRPF quedaría `parcial` para
  siempre.
- Sigue abierto (preexistente, no lo causa esto): el objetivo de recompute es
  `total_eur`, así que una emitida con IRPF conciliada por el importe realmente
  recibido queda `parcial`. Cambiarlo mueve estados en prod y pide migración
  propia con backfill.

Migs 640/641. Ver [[columna-derivada-por-recompute-solo-admite-un-escritor]] ·
[[importe-fiscal-no-es-importe-a-cobrar-retenciones]] · [[facturaia]]
