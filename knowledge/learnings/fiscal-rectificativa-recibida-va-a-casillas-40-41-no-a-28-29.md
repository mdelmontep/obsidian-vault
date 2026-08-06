---
title: un abono de proveedor va a las casillas 40/41 del 303, no restando de 28/29
date: 2026-08-06
source: claude-code-session
tags: [fiscal, iva, modelo-303, aeat, facturaia]
---
Instrucciones AEAT del 303 (2026), verbatim para 40/41 «Rectificación de
deducciones»: *«el importe de la base imponible y de las cuotas deducibles
rectificadas»* y *«si el resultado de la rectificación implica una minoración de
las deducciones, se consignará con signo negativo»*. Las 28/29 son otra cosa:
cuotas soportadas de **operaciones corrientes** del periodo.

**La trampa**: el resultado del periodo sale IGUAL por las dos vías, así que el
error no se ve mirando el importe a pagar. Pero no es solo presentación:
28/29 y 07/09 son `numeric` SIN SIGNO en el registro posicional → con un abono
grande, **el fichero para la AEAT no se genera**.

Límite literal que importa: *«No se incluirán aquellas rectificaciones que hayan
sido regularizadas en autoliquidaciones de periodos anteriores»* → lo ya
declarado (aunque fuera mal) NO se arrastra al trimestre en curso; se corrige
por el periodo afectado.

Emitidas → 14/15, y ahí *«no deberá procederse a desglosar por tipos de
gravamen»*, al revés que 07/09.
Detalle completo (plazos, art. 74 bis RIVA, recargos art. 27 LGT):
`docs/architecture/fiscal-rectificativas-recibidas.md` en el repo.
