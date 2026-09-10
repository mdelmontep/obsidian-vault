---
title: responder un ticket escribiendo la fila entrega el texto y nada más
date: 2026-09-10
source: facturaia
tags: [soporte, side-effects, endpoint, verificacion]
---
Un hilo de soporte parece una tabla: `INSERT` en `feedback_messages` y listo. No lo es. En
TuFacturaIA los efectos de responder viven en el ENDPOINT (`POST /api/admin/feedback/[id]/messages`),
no en un trigger: valida que el adjunto pertenezca a la org del ticket, pone `visto_por_user=false`
(la campanita del cliente), mueve el ticket de `nuevo` a `en_revision` y dispara el email.

Escrita la fila a mano, el cliente **no recibe nada** y el panel enseña una conversación que para
él no existe. La regla general: antes de escribir por SQL algo que la app también escribe, leer
el handler y contar qué más hace; si hace algo más que el INSERT, se conduce la UI real.

Verificar por TRES sitios, que es lo que separa «enviado» de «entregado»: la pantalla, la fila en
Postgres (`autor`, `internal`, `adjunto_path`, estado del ticket) y `email_log` en `delivered`.

Ver [[feedback_smokes_siempre_con_agent_browser]] · [[cerrar-un-ticket-automaticamente-no-es-responder-a-quien-lo-abrio]]
