---
title: Saldo inicial cashflow — coexistencia PSD2 + manual sin conflicto
date: 2026-05-24
source: FacturaIA Cashflow v2.2 commit fbd3a37
tags: [facturaia, cashflow, ux, multi-source-data]
---

# Saldo inicial cashflow — coexistencia PSD2 + manual sin conflicto

Cuando un módulo tiene dos fuentes posibles para el mismo dato (PSD2 automático + manual), la trampa es plantearlas como **competidoras**. El usuario se queda mirando "¿cuál vale, cuál se ignora?" — y si pone la manual, espera que pise la automática.

## Patrón aplicado: el manual cambia de semántica según el contexto

Para evitar el conflicto, **el manual se redefine** cuando coexiste con la fuente automática:

- **Sin PSD2**: el manual representa "el saldo de partida completo". Se usa solo.
- **Con PSD2**: el manual cambia a "otras cuentas / efectivo" — explícitamente "lo que la fuente automática NO ve". **Se suma al PSD2, no compite con él.**

El copy de la UI lo hace evidente sin que el usuario tenga que leer documentación:

> Sin PSD2: 🏦 Indica tu saldo actual
> Con PSD2: 🏦 + Añadir efectivo / otra cuenta

Y la línea de resumen muestra ambos términos con su origen claro:

> Partes de **14.340€** · BBVA · Revolut · +2.000€ otras cuentas/efectivo · actualizado 24 may

## Auto-ajuste resuelve el "se desactualiza"

El otro problema del manual es que el usuario lo pone una vez y se olvida — el dato envejece y el pronóstico miente. Fix: guardar **valor + ancla con fecha**, y derivar el valor mostrado como `valor_ancla + neto_real_desde_ancla`. Si el usuario sigue subiendo facturas/gastos, el saldo derivado se mantiene preciso sin intervención.

## Cuándo NO añadir setting en `/agentes`

La propuesta inicial era exponer el saldo manual en el modal de configuración del módulo (estilo `horizonte_dias` / `cuota_autonomos`). Lo descarté tras ver que:

1. Settings de módulo se configuran 1 vez y se olvidan → saldo se desactualiza.
2. Discoverability mala: el usuario va a `/cashflow` esperando ver el saldo, no a `/agentes`.
3. Inline en `/cashflow` es self-explanatory ("indica tu saldo actual"), no necesita un sitio aparte.

Regla aplicable: si el setting **cambia el dato visible justo encima**, debe estar inline donde se ve. Settings en `/agentes` son para configuración estable (umbrales, toggles binarios, defaults).

## Veredicto

Dos fuentes para el mismo dato pueden coexistir si:
1. **Redefinen su scope cuando coinciden** (manual = "lo que la otra no ve").
2. **El copy lo hace evidente** sin documentación.
3. **La fuente que se desactualiza** se auto-ajusta con la actividad ya registrada.
