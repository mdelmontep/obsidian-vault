---
title: prompts financieros necesitan tabla scoring numérica
date: 2026-04-21
source: claude-code-session
tags: [claude, prompts, facturaia, scoring]
---

Cuando Claude asigna scores de confianza (ej: matching bancario factura↔movimiento), usar tabla de puntos concretos en el prompt:

| Criterio | Puntos |
|----------|--------|
| Importe exacto (±0.05€) | +50 |
| Concepto contiene nombre cliente/proveedor | +25 |
| Concepto contiene número de factura | +30 |
| Fecha dentro de ±7 días del vencimiento | +15 |
| Regla aprendida aplica | +boost |
| Fecha anterior a emisión de factura | -100 |

Sin tabla numérica, Claude genera scores inconsistentes entre llamadas — a veces 85, a veces 60 para el mismo tipo de match.

Score máximo: capear a 100. Incluir valor de penalización (-100) para descartes automáticos.

Comparar siempre contra `factura.total` (con IVA), nunca contra base imponible. Los movimientos bancarios son importes brutos.
