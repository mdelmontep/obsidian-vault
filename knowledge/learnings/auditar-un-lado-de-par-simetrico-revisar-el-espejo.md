---
title: auditar un lado de un par simétrico → grepear el espejo en el mismo PR
date: 2026-06-15
source: claude-code-session
tags: [auditoria, supabase, conciliacion, facturaia, composicion]
---

Cuando un fix cierra un hueco en UNA de dos funciones simétricas, el espejo casi siempre tiene el mismo hueco sin tapar. El audit per-función pasa verde; el par no.

Pares típicos: lado-movimiento vs lado-factura · dos RPCs que asignan estados mutuamente excluyentes · validador de un sentido vs el inverso.

En conciliación TuFacturaIA bitó **3 veces seguidas**:
- mig 283: overpayment sumaba el resto en un lado, no en el otro.
- mig 289: capacidad+resto y guard anticipo arreglados solo en `validate_movimiento_capacity`/`asignar_manual`.
- mig 290: 289 metió `mov_es_anticipo` en `asignar_manual` pero dejó `vincular_transferencia`/`registrar_anticipo` sin guards cruzados.

Regla: al tocar una función de un par simétrico, **grepea el espejo y arréglalo en el mismo PR** (`grep` la otra función + el estado contrario). No esperes a la siguiente auditoría. Enlaza con [[audits-cross-pr-vs-per-pr]].

**2026-07-30 — es el patrón nº1 de la auditoría funcional completa: 6 casos de 400 controles.** Pares nuevos: `ajustar_lote_manual` (bloquea negativo) vs `ajustar_stock_manual` (no lo bloqueaba) · Sidebar desktop vs menú "Más" móvil · `confirmando-cuenta` (comprueba el error de `setSession`) vs `invitacion` (no). El hermano sin guard es siempre el menos transitado, y el que sí lo tiene es el que se prueba primero: por eso la ausencia pasa desapercibida. Lo que cierra la clase entera, no el caso: **fuente única que consuman las dos superficies** (ej. `lib/nav/module-visibility.ts`) + test que compare el veredicto de ambas sobre los mismos N casos. Arreglar solo el hermano deja el par libre de divergir otra vez.
