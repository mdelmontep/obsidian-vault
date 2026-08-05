---
title: columna derivada por un recompute solo admite un escritor; el segundo pierde en silencio
date: 2026-08-06
source: claude-code-session
tags: [postgres, arquitectura, triggers, bd]
---

Si una función `recompute_x()` recalcula una columna DESDE CERO y la escribe,
cualquier otro camino que escriba esa misma columna a mano queda pendiente de un
hilo: el dato sobrevive solo hasta que algo dispare el recálculo.

- Caso TuFacturaIA (mig 640): `recompute_factura_estado` derivaba `estado` de las
  asignaciones bancarias, y `marcarFacturaCobrada` lo escribía a pelo. Un cobro
  marcado a mano se perdía al vincular y desvincular un movimiento — recompute
  corría con 0 asignaciones y dejaba `pendiente` con `fecha_cobro` a NULL. Nadie
  lo borró y no hay traza: el evento de pago nunca existió como fila.
- Fix: el escritor manual deja de escribir la columna y **registra un evento**
  (fila en un ledger) que recompute suma. La columna pasa a tener un solo autor.
- Señal de que estás en este agujero: el flujo A escribe `estado` y el flujo B
  tiene un trigger `AFTER … EXECUTE recompute`. Grep del nombre de la columna en
  los UPDATE del repo — si sale en más de un sitio, uno de los dos va a perder.
- Si necesitas la cifra que recompute calcula (p.ej. cuánto falta por cobrar),
  extráela a una función SQL que **recompute también llame**. Replicarla en la
  app crea la divergencia por la puerta de atrás.

Inverso de [[agregado-cacheado-sobre-ledger-recompute-trigger]] · relacionado con
[[postgres-guard-transition-no-persiste-en-recompute-chain]] · [[triggers-bd-sync-son-antipatron]]
