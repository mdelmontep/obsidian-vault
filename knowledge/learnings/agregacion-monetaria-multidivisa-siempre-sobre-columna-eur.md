---
title: toda suma cross-documento va sobre la columna en EUR, nunca sobre el importe en divisa
date: 2026-07-25
source: claude-code-session
tags: [multidivisa, fiscal, postgres]
---

Con `moneda` + `tipo_cambio` + `total_eur` GENERATED, el bug no es la conversión: es que **9 agregaciones sumaban `total` crudo** (estimación del 303, retenciones IRPF ×2 copias, aging, columnas de clientes/proveedores, notificaciones, insights). Estaban "correctas por accidente" porque casi todo era EUR: arreglar el dato de divisa es lo que **crea** la exposición, así que van en el mismo lote o el fix empeora las cifras.

- Suma cross-documento → `COALESCE(total_eur, total)`. Display de UN documento → su divisa **más** el equivalente EUR (`73,96 US$ · ≈ 64,61 €`), nunca `fmt2` a secas, que hardcodea `€`.
- Fallback `?? total`, no columna obligatoria: si no, rompes todos los fixtures existentes.
- El equivalente que se muestra tiene que ser la MISMA columna contra la que casa el motor de conciliación; derivarlo aparte garantiza que un día no cuadren.
- Test de arquitectura barato: ningún `.select()` sobre facturas que pida `total` sin pedir `total_eur`.

Nació en TuFacturaIA, ver [[facturaia]].
