---
title: redirigir un envío a otro destinatario arrastra su gate de verificación
date: 2026-07-29
source: claude-code-session
tags: [whatsapp, compliance, producto, cobros]
---
"Que el recordatorio vaya al contacto principal en vez de al cliente" parece un
cambio de una línea: sustituir de dónde sale el teléfono. No lo es. El envío por
WhatsApp estaba detrás de un gate (`telefono_validado_at` del cliente) que existe
por las condiciones de Meta: escribir a un número no verificado arriesga el número
de la organización. El contacto no tenía ese campo, así que cumplir la petición
al pie de la letra habría sido saltarse el gate sin que nadie lo notara.

Patrón: al mover un envío a otra entidad, la pregunta no es "¿tiene el dato?" sino
"¿arrastra también las condiciones bajo las que ese dato podía usarse?" (verificación,
consentimiento, opt-out, cuota). Si la entidad nueva no las tiene, se le añaden;
si no, se cae a la anterior.

Y decidir POR CANAL, no por persona: un contacto puede tener email y no teléfono
verificado, así que el correo va a él y el WhatsApp sigue yendo al cliente. Tratar
"destinatario" como una sola cosa fuerza a elegir entre no cumplir o no cambiar nada.

Caso real: TuFacturaIA migs 590/591. Efecto del despliegue: el email cambia solo,
el WhatsApp no se mueve hasta que alguien valide cada contacto a mano.
