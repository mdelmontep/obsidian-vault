---
title: documento que representa dinero ya cobrado debe marcarse cobrada explícito
date: 2026-07-01
source: claude-code-session
tags: [facturaia, estado-machine, kpis, bug]
---

Un motor de creación de documentos (`createDocument` en TuFacturaIA) por defecto deja
cualquier factura en `estado='pendiente'` salvo aviso contrario — nunca infiere "cobrada"
por sí solo. Si el flujo que llama representa dinero YA cobrado en el momento (venta
instantánea, ticket en efectivo/Bizum), y no llamas explícitamente a la función que marca
cobrado (`marcarFacturaCobrada`), el documento queda "pendiente" para siempre.

El bug es silencioso porque ningún test de creación falla — el documento se crea bien,
tiene PDF, numeración correcta. El daño aparece aguas abajo: KPIs de dashboard, cashflow,
aging widgets y crons de vencidas normalmente filtran solo por `estado` (nunca por el tipo
de documento), así que el dinero ya cobrado aparece como "por cobrar" y acaba "vencido".

Fix: tras crear el documento, llamar a la función de "marcar cobrado" existente (no
reimplementar la transición de estado) siempre que el flujo represente un cobro ya recibido.

Generalizable: en cualquier app con máquina de estados pendiente/cobrado, un flujo de "cobro
instantáneo" nuevo NO hereda automáticamente el estado correcto del motor genérico de
creación — hay que forzarlo explícitamente en ese flujo concreto.
