---
title: feature de pago atada a una capacidad que el plan ya concede → inclúyela en ese plan, no la cobres aparte
date: 2026-06-05
source: claude-code-session
tags: [pricing, saas, producto]
---
Caso real (TuFacturaIA): el plan Pro daba cuota de 2 empresas, pero el módulo de
consolidación (`multiempresa`: comparar/agregar varias empresas) era enterprise-only
→ un Pro podía CREAR 2 empresas pero recibía 403 al verlas juntas. Incoherencia: la
feature estaba atada a una capacidad que el plan ya concedía.

Regla: si una feature de pago solo tiene sentido cuando ya tienes una capacidad que
el plan incluye (cuota > 1, N usuarios, etc.), inclúyela en ese plan. Cobrarla aparte
no genera ingreso, genera churn/desconfianza ("me dejas tener 2 pero me cobras por
compararlas"). Diferencia el plan superior por VOLUMEN u otras features, no por
desbloquear el uso natural de lo que el plan inferior ya da.

Detección: cruzar la tabla de cuotas/límites por plan contra la tabla de features por
plan; toda fila donde "puede crear N>1 de X" pero "feature que opera N de X" está en
plan superior es candidata a bug de pricing. Fix = un upsert en `plan_features`
(`ON CONFLICT DO UPDATE`, no DO NOTHING). Ver [[ADR-028-multiempresa-scope-navegar-agregar-cobrar]].
