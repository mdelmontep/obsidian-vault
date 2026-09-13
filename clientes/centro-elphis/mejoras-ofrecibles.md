---
title: Mejoras ofrecibles a Centro Elphis (no pedidas)
date: 2026-09-07
source: centro-elphis
tags: [elphis, producto, backlog-comercial, whatsapp]
---

Cosas técnicamente listas o casi listas que **la clienta no ha pedido**. No se implementan; se guardan para ofrecerlas cuando encaje. Distinto de [[bloqueantes-elphis]], que sí bloquea trabajo en curso.

## Recordatorio del enlace de reserva a las 24 h

**Qué sería:** hoy el bot manda el enlace de Doctoralia y ahí termina. Quien recibe el enlace y no reserva se pierde sin más. El recordatorio sería un segundo WhatsApp a las 24 h solo a esos casos, con el libro de envíos (`booking_links`) para saber a quién se le mandó y quién no confirmó.

**Por qué no está hecho (7-sep-2026):** decisión de Manu — "no lo han pedido". Se descartó del plan de mejora y **ni siquiera se crearon las columnas** `reminder_due_at / reminder_sent_at / reminder_meta_message_id / reminder_error` en `booking_links`, precisamente para que nadie pueda encenderlo por error.

**Qué costaría de verdad:** no es solo código. Es un mensaje no solicitado a un paciente, o sea marketing para Meta → **plantilla HSM nueva y aprobada**, distinta de las 3 que ya hay ([[whatsapp-fuera-ventana-24h-requiere-plantilla-hsm]]), y utility no cuela para esto ([[whatsapp-recordatorio-diferido-siempre-plantilla-utility]]). Más el OK de Alba: es un centro de adicciones y un recordatorio identifica al destinatario como paciente ante quien vea el móvil.

**Si algún día se ofrece:** ventana horaria obligatoria, o escribe de madrugada ([[recordatorio-relativo-sin-ventana-horaria-escribe-de-madrugada]]).

Relacionado: [[bloqueantes-elphis]], [[index]].
