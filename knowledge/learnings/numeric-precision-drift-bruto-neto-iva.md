---
title: numeric(x,2) genera drift inevitable convirtiendo bruto↔neto con iva
date: 2026-05-25
source: claude-code-session
tags: [postgres, fiscal, redondeo, numeric]
---

Caso real TuFacturaIA 2026-05-25: user pone 10€ bruto con IVA 21%. Sistema persiste precio_unitario neto = 10/1.21 = 8.264462... → guarda 8.26 en NUMERIC(12,2) → al reconstruir total muestra 8.26 × 1.21 = 9.9946 ≈ **9.99€**. Imposible cuadrar a 10.00 con solo 2 decimales — ningún valor de 2 dec (8.26 ni 8.27) da exactamente 10.

**Fix**: ampliar a NUMERIC(14,6) (mig 164). Permite persistir 8.264463 → total reconstruido = 10.0000003 ≈ 10.00. Cast `NUMERIC(12,2) → NUMERIC(14,6)` es ampliación sin pérdida (datos existentes intactos).

**Aplica a cualquier app** con cálculo bruto→neto→bruto y persistencia en BD. Patrones de mitigación:

- Persistir EN base neta con ≥4-6 decimales si la UI muestra brutos.
- O persistir el TOTAL bruto + porcentaje y derivar la base on-read.
- O aceptar drift ≤1 céntimo agregado (AEAT lo permite por tipo IVA, Reglamento Verifactu).

Helper `calcularLinea` debe trabajar desde el TOTAL cuando inclusive=true: derivar base = round(total/(1+iva/100)) + cuota = total − base → garantiza base+cuota = totalBruto exacto. No redondear precioBase intermedio.
