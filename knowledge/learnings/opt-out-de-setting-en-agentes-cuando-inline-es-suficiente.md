---
title: Setting en /agentes vs inline — cuándo elegir cuál
date: 2026-05-24
source: TuFacturaIA Cashflow v2.2 commit fbd3a37
tags: [facturaia, ux, settings-pattern]
---

# Setting en `/agentes` vs inline — cuándo elegir cuál

TuFacturaIA tiene un patrón de "settings de módulo" en `/agentes` (modal `ModuloConfig` que renderiza dinámicamente cualquier campo del `configSchemaDefault`). Es tentador meter ahí cualquier opción nueva — "es el sitio canónico, allá va".

Pero tiene un coste: lo que vive en `/agentes` se configura **una vez** y se olvida. Si el dato necesita mantenerse al día, ahí muere.

## Heurística

| Vive en `/agentes` | Vive inline en la vista del módulo |
|---|---|
| Toggle binario (`incluir_fiscal`, `incluir_recurrentes`) | Dato que el usuario verá afectar la vista inmediatamente |
| Umbral fijo (`umbral_alerta_caja`, `horizonte_dias`) | Dato que cambia con el tiempo (saldo bancario manual) |
| Selectores predefinidos (`cuota_autonomos` presets RETA) | Importes específicos que el usuario revisa |
| Configuración estable que se decide al activar el módulo | Acción rápida que se ejecuta varias veces |

## Caso real: saldo inicial cashflow

Propuesta inicial: campo `saldo_inicial` en `configSchemaDefault` → renderizado automático en `/agentes` modal Cashflow → usuario edita y guarda.

Problema: el saldo bancario cambia cada día. El usuario lo pone hoy `5.000€`, mañana son `4.200€` y el pronóstico miente. Settings en `/agentes` invitan a "configurar y olvidar".

Fix aplicado: editor inline en `/cashflow` mismo + auto-ajuste vía `valor_ancla + neto_real_post_ancla`. El usuario lo configura **donde lo ve** y el sistema mantiene el dato vivo sin pedir actualizaciones manuales.

## Regla general

Si el setting **cambia el dato visible justo encima**, debe estar inline. Si el setting **modela una preferencia estable del usuario**, va a `/agentes`.

## Conexión

Va con [[saldo-inicial-cashflow-coexistencia-psd2-manual]].
