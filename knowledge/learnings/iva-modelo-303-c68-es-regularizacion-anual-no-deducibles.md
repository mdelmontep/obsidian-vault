---
name: iva-modelo-303-c68-es-regularizacion-anual-no-deducibles
description: Bug clásico fórmula 303 — c68 es regularización anual (solo 4T/12), NO total deducibles. Confusión infla c69 x2 en AIB intracom.
date: 2026-05-22
source: claude-code-session
tags: [aeat, iva, modelo-303, fiscal]
---

**Síntoma**: AIB intracom recibido (operación neutra fiscal: devengo + deducible mismo importe) → cliente paga IVA por una operación que debe ser 0€.

**Causa**: muchos calculadores asumen `c69 = c66 + c77 − c78 + c68 + c108` interpretando `c68` como "total cuotas deducibles". **AEAT verbatim** (instrucciones 303-2026): c68 = "Regularización anual" — solo aplica en 4T trimestral o periodo 12 mensual cuando hay prorrata o cambio de régimen.

**Fórmula correcta** verbatim:
- c27 = Σ cuotas devengadas (emitidas + AIB devengado)
- c45 = Σ cuotas deducibles (recibidas + AIB deducible)
- c46 = c27 − c45 (régimen general)
- c64 = c46 + c58 + c76 (suma con simplificado + concursos)
- c66 = c64 (territorio único, c65=100)
- c69 = c66 + c77 − c78 + c68 + c108

**Ejemplo numérico bug**: AIB DE base 2000€ IVA 21% (=420€ devengo + 420€ deducible neto 0):
- Bug: c69 = 0 + 420 + 0 + 420 + 0 + 0 = 840€ a ingresar ❌
- Correcto: c46 = 420 − 420 = 0, c69 = 0 ✅

Aplica a cualquier dev IVA España 2026.
