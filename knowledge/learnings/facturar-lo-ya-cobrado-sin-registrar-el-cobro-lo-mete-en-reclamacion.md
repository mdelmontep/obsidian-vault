---
title: emitir la factura de un cobro ya hecho sin registrar el cobro la mete en reclamación
date: 2026-08-18
source: claude-code-session
tags: [facturacion, stripe, billing, integraciones]
---

Cuando un webhook de pago (Stripe `invoice.paid`, un TPV, un banco) dispara la emisión de una
factura, el dinero **ya está cobrado**: la factura nace saldada. Pero el orquestador de emisión
normal deja el documento en `pendiente`, porque en el flujo humano lo normal es emitir y esperar.

Consecuencia: esa factura entra en el aging, en el cron de vencimientos y en el circuito de
recordatorios, y **el sistema le reclama por email un pago que el cliente ya hizo con tarjeta**.
No falla nada, no salta ninguna alerta: es el peor tipo de defecto de una integración de cobro.

Patrón: emisión y registro del cobro son **un solo paso**, no dos. Y el cobro se registra por la
puerta que tenga el proyecto (ledger de pagos), sin escribir a mano el estado ni la fecha de cobro
si son derivadas.

Dos cabos que casi siempre se olvidan en el mismo sitio: el `origen` del cobro suele ser un enum
CERRADO (hay que añadir el valor nuevo y **todos** sus espejos: CHECK, tipo TS, etiqueta de UI), y
el vencimiento por defecto (+30 días) hay que fijarlo a la fecha del cobro o la factura nace
vencida a futuro estando pagada.
