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
