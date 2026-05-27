---
title: ADR-022 — Facturas en divisa extranjera: equivalente EUR congelado + agregar siempre en EUR
date: 2026-05-27
status: accepted
tags: [adr, facturaia]
---

## Contexto
`facturas.moneda` existía suelta (sin tipo de cambio, sin constraint) y TODAS las sumas (dashboard, cashflow, **modelo 303**) sumaban `total` mezclando divisas (100 USD + 100 EUR = 200). Error de corrección fiscal. Producto español: clientes que facturan a USA/UK existen pero son minoría.

## Opciones consideradas
- **A — Soporte ES correcto**: `moneda` + `tipo_cambio` congelado a devengo (BCE híbrido auto/manual) + `base_eur`/`total_eur` generadas; agregar siempre en EUR.
- **B — Bloquear a EUR**: CHECK `moneda='EUR'`, cerrar la trampa. Mínimo esfuerzo pero no sirve a quien factura fuera.
- **C — Multi-divisa completo**: ledgers por divisa, switcher, FX gain/loss. Semanas; sobredimensionado.

## Decisión
**A**, porque cumple RD 1619/2012 art 6.1.j (cuota IVA expresada en EUR al tipo de devengo) sin la complejidad de C. Tipo de cambio del BCE vía Frankfurter, congelado en el documento. EUR equivalente como columnas generadas (ver [[columna-generada-stored-para-equivalente-derivado]]).

## Consecuencias
Toda agregación nueva DEBE sumar `*_eur`. El documento/PDF va en divisa original + bloque de equivalencia EUR. **VeriFACTU + divisa extranjera queda DIFERIDO** (la huella AEAT sigue sobre `total` original; revisión fiscal aparte antes de habilitar). Añadir divisa = editar `SUPPORTED_CURRENCIES` + CHECK (misma lista en dos sitios).
