---
title: un seed repartido entre un trigger y el onboarding crea entidades a medias
date: 2026-07-29
source: claude-code-session
tags: [postgres, onboarding, multi-tenant, supabase]
---
Las series de numeración de una organización se sembraban en DOS sitios: un trigger
`AFTER INSERT` (tres series) y la función del onboarding de usuario (las otras cuatro).
Una organización creada por script, migración de datos o a mano recibe solo la mitad,
y el síntoma llega semanas después: al emitir, la función de numeración lanza "Serie no
encontrada" y el endpoint devuelve un 500 genérico, imposible de diagnosticar desde fuera.

Lo llamativo es que ya había mordido: una migración anterior hizo el backfill por este
mismo motivo, con el síntoma descrito en su cabecera, pero como arreglo puntual. No cerró
la puerta, así que volvió a entrar la siguiente entidad creada por script.

Regla: si el alta de una entidad necesita filas hijas para funcionar, **todas** se siembran
en el mismo sitio, y ese sitio es el trigger de alta (que no se puede saltar), no el flujo
de UI. Un backfill sin cerrar el origen es un parche con fecha de caducidad.

Cómo detectarlo: buscar entidades a las que les falte alguna fila hija canónica
(`having not bool_or(hijo.codigo = 'X')`). Caso real: TuFacturaIA migs 402 (parche) y 589
(cierre), destapado al intentar emitir una factura de prueba en una org creada por script.
